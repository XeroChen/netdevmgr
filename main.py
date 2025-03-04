# -*- coding: utf-8 -*-

from ethernet.eth_card import NetIfaces
from pci.pci_ids import PCIIds
from pci.pci_dev import PCIDevice
from pci.pci_dev import PCIDeviceDataBase

def main():
    # PciDB = PCIDeviceDataBase()
    # PciDB.get_from_lspci()

    # PCIIdsDB = PCIIds()
    
    # for pci_addr, pci_device in PciDB.devices.items():
    #     if pci_device.class_code == "0200":
    #         print(f"-------------------------------------------------------------------------------------------------")
    #         print(f"PCI Address: {pci_addr}")
    #         print(f"Vendor ID: {pci_device.vendor_id} {PCIIdsDB.get_vendor_name(pci_device.vendor_id)}")
    #         print(f"Device ID: {pci_device.device_id} {PCIIdsDB.get_device_name(pci_device.vendor_id, pci_device.device_id)}")
    #         print(f"Class Code: {pci_device.class_code}")
    #         print(f"Bus: {pci_device.bus}, Slot: {pci_device.slot}, Function: {pci_device.function}")
    #         print(f"Driver Name: {pci_device.get_device_driver()}")
    #         print(f"Driver Module: {pci_device.get_driver_kmod_info()}")

    pciids = PCIIds()
    netifs = NetIfaces()
    netifs.get_ifaces()
    for idx, iface in netifs.ifaces.items():
        print("-------------------------------------------------------------------------------------------------")
        print(f"Interface Name: {iface.name}")
        print(f"Index: {iface.index}, MAC: {iface.mac}, IP: {iface.ip}, IPv6: {iface.ipv6}")
        IfacePCI = iface.get_pci_dev()
        if IfacePCI:
            print(f"Associated PCI device: {IfacePCI.get_pci_bus_addr()}")
            print(f"Vendor ID: ({IfacePCI.vendor_id}) {pciids.get_vendor_name(IfacePCI.vendor_id)}")
            print(f"Device ID: ({IfacePCI.device_id}) {pciids.get_device_name(IfacePCI.vendor_id, IfacePCI.device_id)}")
            print(f"Class Code: {IfacePCI.class_code}")
            print(f"Bus: {IfacePCI.bus}, Slot: {IfacePCI.slot}, Function: {IfacePCI.function}")
            print(f"Driver Name: {IfacePCI.get_device_driver()}")
            print(f"Driver Module: {IfacePCI.get_driver_kmod_info()}")
            print(f"Firmware: {iface.get_firmware_version()}")

if __name__ == "__main__":
    main()