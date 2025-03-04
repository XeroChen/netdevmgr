# -*- coding: utf-8 -*-
import os
import subprocess
"""
A class representing a PCI (Peripheral Component Interconnect) device.

import subprocess

import subprocess

This class encapsulates information about a PCI device including its vendor ID,
device ID, class code, and location on the PCI bus (bus number, slot number,
and function number).

Attributes:
    vendor_id (str): The vendor ID of the PCI device
    device_id (str): The device ID of the PCI device
    class_code (str): The class code of the PCI device
    bus (int): The bus number where the device is located
    slot (int): The slot number where the device is located
    function (int): The function number of the device

Methods:
    __str__(): Returns a string representation of the PCI device
    get_device_info(): Returns a dictionary containing all device information
"""

class PCIDevice:
    def __init__(self, vendor_id, device_id, class_code, bus, slot, function):
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.class_code = class_code
        self.bus = bus
        self.slot = slot
        self.function = function

    def __str__(self):
        return (f"PCI Device [Vendor ID: {self.vendor_id}, Device ID: {self.device_id}, "
                f"Class Code: {self.class_code}, Bus: {self.bus}, Slot: {self.slot}, "
                f"Function: {self.function}]")

    def get_device_info(self):
        return {
            "vendor_id": self.vendor_id,
            "device_id": self.device_id,
            "class_code": self.class_code,
            "bus": self.bus,
            "slot": self.slot,
            "function": self.function
        }
    
    def get_pci_bus_addr(self):
        return f"0000:{self.bus:02x}:{self.slot:02x}.{self.function}"

    def get_device_driver(self):
        try:
            driver_path = f"/sys/bus/pci/devices/{self.get_pci_bus_addr()}/driver"
            return os.path.basename(os.readlink(driver_path))
        except (FileNotFoundError, OSError):
            return None
    
    def get_driver_kmod_info(self):
        driver = self.get_device_driver()
        if driver:
            try:
                modinfo_output = subprocess.check_output(["modinfo", driver], encoding="utf-8")
                # get the filepath of the driver module
                modinfo_filename_line = modinfo_output.splitlines()[0]
                if modinfo_filename_line.startswith("filename:"):
                    modinfo_filename = modinfo_filename_line.split(":")[1].strip()
                else:
                    modinfo_filename = "Unknown"

                # get the version of the driver module
                modinfo_version_line = modinfo_output.splitlines()[1]
                if modinfo_version_line.startswith("version:"):
                    modinfo_version = modinfo_version_line.split(":")[1].strip()
                else:
                    modinfo_version = "Unknown"
                return modinfo_filename, modinfo_version
            except subprocess.CalledProcessError as e:
                return f"Error running modinfo: {e} \n{modinfo_output}"
        return None

class PCIDeviceDataBase:
    def __init__(self):
        self.devices = {}
    
    def add_device(self, device: PCIDevice):
        self.devices[device.get_pci_bus_addr()] = device
    
    def get_from_lspci(self):
        try:
            # execute `lspci -nn` and parse the output of the command

            lspci_output = subprocess.check_output(["lspci", "-n"], encoding="utf-8")
            for line in lspci_output.splitlines():
                if not line:
                    continue
                parts = line.split(" ")
                pci_addr = parts[0]
                vendor_id, device_id = parts[2].split(":")
                class_code = parts[1].split(":")[0]
                bus = int(pci_addr.split(":")[0], 16)
                slot = int(pci_addr.split(":")[1].split(".")[0], 16)
                function = int(pci_addr.split(".")[1])
                self.add_device(PCIDevice(vendor_id, device_id, class_code, bus, slot, function))
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running lspci: {e}")

    def print_devices(self):
        for pci_addr, device in self.devices.items():
            print(f"PCI Address: {pci_addr}")
            print(f"Vendor ID: {device.vendor_id} ")
            print(f"Device ID: {device.device_id} ")
            print(f"Class Code: {device.class_code}")
            print(f"Bus: {device.bus}, Slot: {device.slot}, Function: {device.function}")

    