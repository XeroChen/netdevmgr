import os
import re
import subprocess
from typing import Dict
from pci.pci_dev import PCIDevice

class NetIf:
    def __init__(self, index, name, mac, ip: list = [], ipv6: list = [], pci_addr: str = None, type: str = "Ethernet"):
        self.index = index
        self.name = name
        self.mac = mac
        self.ip = ip
        self.ipv6 = ipv6
        self.pci_addr = self.get_pci_addr()

    def __str__(self):
        return f"NetIf [Idx: {self.index} Name: {self.name}, MAC: {self.mac}, IP: {self.ip}]"
    
    def __repr__(self):
        return self.__str__()
    
    def get_pci_addr(self):
        if self.name == "lo":
            return ""
        try:
            output = subprocess.check_output(["ethtool", "-i", self.name], text=True)
            for line in output.splitlines():
                if "bus-info: " in line:
                    pci_addr = line.split(": ")[1].strip()
                    if pci_addr != "0000:00:00.0" and pci_addr != "N/A":
                        return pci_addr
        except subprocess.CalledProcessError:
            pass
        return None
    
    # Get the firmware version of the interface
    def get_firmware_version(self):
        try:
            output = subprocess.check_output(["ethtool", "-i", self.name], text=True)
            for line in output.splitlines():
                if "firmware-version: " in line:
                    return line.split(": ")[1].strip()
        except subprocess.CalledProcessError:
            pass
        return
    
    # Get the PCI device object for the interface
    def get_pci_dev(self) -> PCIDevice:
        if self.pci_addr:
            # get bus, slot and function from pci address like 0000:00:00.0
            _, bus, dev = self.pci_addr.split(":")
            slot, function = dev.split(".")

            # get numeric values for bus, slot and function
            bus = int(bus, 16)
            slot = int(slot, 16)
            function = int(function)

            # get numeric values for vendor and device id from lspci
            try:
                lspci_output = subprocess.check_output(["lspci", "-n", "-s", self.pci_addr], text=True)
                vendor_id, device_id = lspci_output.split()[2].split(":")
                class_code = lspci_output.split()[1].split(":")[0]
                # Create a PCIDevice object with the parsed information
                return PCIDevice(vendor_id, device_id, class_code, bus, slot, function)
            except subprocess.CalledProcessError:
                return None
    
    # Bring up or down an interface by its name and returns whether the operation was successful
    def link_up_down(self, up: bool):
        if up:
            return self._link_up(self.name)
        else:
            return self._link_down(self.name)
        
    def _link_up(self):
        try:
            subprocess.check_output(["ip", "link", "set", self.name, "up"])
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _link_down(self):
        try:
            subprocess.check_output(["ip", "link", "set", self.name, "down"])
            return True
        except subprocess.CalledProcessError:
            return False
    
class NetIfaces:
    def __init__(self):
        self.ifaces = dict()

    # Parse the output of ip addr show to get the ifindex, ifname, mac, ip and ip6 addresses
    # for each interface on the system
    # fill in the NetIf object with the parsed information
    # Note: One interface may have multiple IP addresses
    def _parse_iface_info(self, iface_info):
        ifindex = None
        ifname = None
        mac = None
        for line in iface_info.splitlines():
            
            if line_prefix := re.match(r"^\d+: \w+", line):
                # recode the ifindex and ifname
                ifindex = int(line_prefix.group().split(":")[0])
                ifname = line_prefix.group().split(":")[1].strip()
                continue

            if "link/ether" in line or "link/loopback" in line:
                mac = line.split()[1]
                
            if ifindex and ifindex not in self.ifaces:
                self.ifaces[ifindex] = NetIf(ifindex, ifname, mac, [], [])
                continue
            
            if "inet6 " in line:
                self.ifaces[ifindex].ipv6.append(line.split()[1])
                continue

            if "inet " in line:
                self.ifaces[ifindex].ip.append(line.split()[1])
                continue

    def get_ifaces(self):
        # parse output of ip addr show to get every iface's ifindex, ip/ip6 and mac addresses
        try:
            output = subprocess.check_output(["ip", "addr", "show"], text=True)
            self._parse_iface_info(output)
        except subprocess.CalledProcessError:
            pass
    
    def get_iface_by_pci_addr(self, pci_addr: str) -> NetIf:
        for idx, iface in self.ifaces.items():
            if iface.pci_addr == pci_addr:
                return iface
        return None
    
        
