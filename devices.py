# General
import time
import json

# import bluetooth
from pygatt import *
from gattlib import DiscoveryService
# from bluetooth.ble import DiscoveryService

# Own modules
import device

class BlueDevices(object):
	"""docstring for BlueDevices"""
	def __init__(self):
		super(BlueDevices, self).__init__()
		self.service = DiscoveryService("hci0")
		print("Init BLE connection module..")

	def search_BLE(self):
		print("Searching bluetooth devices")
		self.devices = self.service.discover(2)
		print("Done..\nFound devices:")
		i = 0
		for address, name in self.devices.items():
			if name == "":
				name = "No name"
			print("{}. Name: {}, address: {}".format(i, name, address))
			i += 1

	def get_device(self, num):
		for address, data in self.devices.items():
			dev_num = data['num']
			if dev_num == num:
				return_data = self.devices[address]
				return_data['address'] = address
				return return_data
		return None

	def get_iaqp_device(self):
		return_data = []
		for address, name in self.devices.items():
			if "IAQ Sensor" in name:
				return_dev = self.devices[address]
				print(return_dev)
				return_data.append(return_dev)
		return return_data
		
	def print_devices(self):
		for address, name in self.devices.items():
			if name == "":
				name = "No name"
			print("Name: {}, address: {}".format(name, address))
		print("\n")

