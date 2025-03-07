# Network Interface and PCI Device Information Tool

A Python tool for gathering and displaying detailed information about network interfaces and their associated PCI devices on Linux systems.

## Overview

This tool provides comprehensive information about network interfaces on a Linux system, including:

- Interface names, indices, MAC addresses, IP addresses (IPv4 and IPv6)
- PCI bus information (address, vendor, device)
- Driver details (name, module path, version)
- Firmware version

It uses system utilities like `ip`, `ethtool`, `lspci`, and Linux's `/sys` filesystem to gather hardware and driver information.

## Requirements

- Linux operating system
- Python 3.6+
- System utilities:
  - `ip` (part of iproute2 package)
  - `ethtool`
  - `lspci` (part of pciutils package)
  - `modinfo` (part of kmod package)
- Access to `/usr/share/hwdata/pci.ids` for PCI vendor/device lookups

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/network-pci-info.git
   cd network-pci-info
   ```

2. Ensure you have the required system utilities:
   ```bash
   sudo apt-get install iproute2 ethtool pciutils kmod
   ```

## Usage

Run the main script to display information about all network interfaces:

```bash
python main.py
```

### Example Output

```
-------------------------------------------------------------------------------------------------
Interface Name: eth0
Index: 2, MAC: 00:1a:2b:3c:4d:5e, IP: ['192.168.1.10/24'], IPv6: ['fe80::21a:2bff:fe3c:4d5e/64']
Associated PCI device: 0000:03:00.0
Vendor ID: (8086) Intel Corporation
Device ID: (1533) I210 Gigabit Network Connection
Class Code: 0200
Bus: 3, Slot: 0, Function: 0
Driver Name: igb
Driver Module: (/lib/modules/5.15.0-76-generic/kernel/drivers/net/ethernet/intel/igb/igb.ko, 5.15.0-76-generic)
Firmware: 0.6-1
-------------------------------------------------------------------------------------------------
Interface Name: lo
Index: 1, MAC: 00:00:00:00:00:00, IP: ['127.0.0.1/8'], IPv6: ['::1/128']
```

## Project Structure

- `main.py` - The main script that demonstrates the tool's functionality
- `ethernet/` - Package for network interface related classes
  - `eth_card.py` - Contains `NetIf` and `NetIfaces` classes for network interface information
- `pci/` - Package for PCI device related classes
  - `pci_dev.py` - Contains `PCIDevice` and `PCIDeviceDataBase` classes
  - `pci_ids.py` - Parses vendor and device information from the PCI ID database

## Classes and Components

### Network Interface Classes

- `NetIf`: Represents a single network interface with methods to:
  - Get the associated PCI address
  - Get firmware version
  - Get the associated PCI device
  - Bring interfaces up or down

### PCI Device Classes

- `PCIDevice`: Represents a PCI device with:
  - Vendor ID, device ID, class code
  - Bus, slot, and function information
  - Methods to get driver information

- `PCIIds`: Parses the PCI IDs database to:
  - Look up vendor and device names based on their IDs
  - Provide human-readable information for PCI devices

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- This tool utilizes Linux system utilities and the PCI IDs database
