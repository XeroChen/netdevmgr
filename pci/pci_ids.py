# -*- coding: utf-8 -*-

class PCIIds:
    def __init__(self, pci_ids_path="/usr/share/hwdata/pci.ids"):
        self.vendors = {}
        self.load_pci_ids(pci_ids_path)

    def load_pci_ids(self, path="/usr/share/hwdata/pci.ids"):
        try:
            current_vendor = None
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip()

                    if not line:
                        continue

                    if line.startswith('C'):
                        continue

                    if line.startswith('#'):
                        continue

                    if line.startswith('\t\t'):
                        continue

                    if not line.startswith('\t'):
                        # Vendor line
                        vendor_id, vendor_name = line.split('  ', 1)
                        vendor_id = vendor_id.strip()
                        self.vendors[vendor_id] = {'name': vendor_name.strip(), 'devices': {}}
                        current_vendor = vendor_id
                    elif line.startswith('\t') and current_vendor:
                        # Device line
                        device_info = line.strip()
                        device_id, device_name = device_info.split('  ', 1)
                        self.vendors[current_vendor]['devices'][device_id] = device_name.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"PCI IDs file not found at {path}")

    def get_vendor_name(self, vendor_id):
        vendor_id = vendor_id.lower()
        if vendor_id in self.vendors:
            return self.vendors[vendor_id]['name']
        return "Unknown vendor"

    def get_device_name(self, vendor_id, device_id):
        vendor_id = vendor_id.lower()
        device_id = device_id.lower()
        if vendor_id in self.vendors and device_id in self.vendors[vendor_id]['devices']:
            return self.vendors[vendor_id]['devices'][device_id]
        return "Unknown device"