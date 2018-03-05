#import pygatt
import sys
import time
from gattlib import GATTRequester, GATTResponse
import xml.etree.ElementTree

class Device(object):
	"""docstring for Device"""
	def __init__(self, device):
		print(device)
		self.settings_file = 'settings.xml'
		self.name = device['name'] 
		self.address = device['address']
		self.uuids = []
		self.appearance = device['appearance']
		self.primary = None
		self.requester = GATTRequester(self.address, False)
		self.status = False
		self.channel = None
		self.loaded_uuids =  []
		self.load_uuids()

	def print_device(self):
		print("Bluetooth device name: {0}, addres: {1}".format(self.name, self.address))

	def connect(self):
		print("Connecting: {}".format(self.name))
		sys.stdout.flush()
		try:
			self.requester.connect(True, 'random')
			print("OK!")
		except:
			print("Connecting failed.")
			self.requester.disconnect()
   
	def reconnect(self):
		print("Reconnecting: {}".format(self.name))
		sys.stdout.flush()
		try:
			self.requester.connect(True, 'random')
			print("OK!")
		except:
			print("Device not avaible.")
			
	def disconnect(self):
		print("Disconnecting: {}".format(self.name))
		sys.stdout.flush()
		
		timeout = time.time() + 5
		while self.requester.is_connected():
			self.requester.disconnect()
			time.sleep(1)
			if time.time() > timeout:
				break
		print("OK!")

	def check_connection(self):
		status = "connected" if self.requester.is_connected() else "not connected"
		print("Checking current status: {}".format(status))
		time.sleep(1)
		if status is "connected":
			self.status = True
		else:
			self.status = False

	def search_services(self):
		print("Searching services..")
		self.primary = self.requester.discover_primary()
		print("Services:")
		for prim in self.primary:
			print(prim)
		print("Done!")

	def load_characteristics(self):
		"""
		- Loads characteristics from IAQP device
		- If not, loads uuids from settings fiel
		- Compares uuids and characteristics and add key value pairs to uuids list
		- Adds uuids to channel
		"""
		if not self.channel:
			raise ChannelNotInitializedError("Channel must be initialised before 'load_characteristics'")

		print("Characteristics:")
		self.characteristics = self.requester.discover_characteristics()
		for char in self.characteristics:
			print(char)
		print("Done!")

		if not self.loaded_uuids:
			self.load_uuids()

		for char in self.characteristics:
			for uuid in self.loaded_uuids:
				if uuid['name'] in char['uuid']:
					uuid['long'] = char['uuid']
					self.uuids.append(uuid)


	def init_channel(self, channel):
		self.channel = channel

	def request_data(self):
		response = GATTResponse()
		try:
			for uuid in self.uuids:
				print("Requesting data with uuid {}..".format(uuid['name'])) 
				raw_data = self.requester.read_by_uuid(uuid['long'])[0]
				bitlist_data = list(map(ord, raw_data)) #This is magic, converts char to list if 8bit integers
				data = 0
				for i in range(len(bitlist_data)) :
					data |= bitlist_data[i]<<(8*i)
				print("Raw data: {}, data in int: {}".format(raw_data, data))
				value = float(data) * uuid['factor']
				print(uuid['sensor'] + ' ' + str(value) + ' ' + uuid['unit'])
				self.channel.add_to_buffer(uuid['field'], value)
		except RuntimeError:
			self.reconnect()
			print("Connection to device lost, trying again in next run!")

	def load_uuids(self):
		parsed_file = xml.etree.ElementTree.parse(self.settings_file).getroot()
		uuid_root = parsed_file.find('uuids')
		for atype in uuid_root.findall('uuid'):
			new_uuid = {}
			new_uuid['name'] = atype.find('name').text
			new_uuid['sensor'] = atype.find('sensor').text
			new_uuid['location'] = atype.find('location').text
			new_uuid['data_type'] = atype.find('data_type').text
			new_uuid['field'] = int(atype.find('field').text)
			new_uuid['factor'] =  float(atype.find('factor').text)
			new_uuid['unit'] =  atype.find('unit').text
			self.loaded_uuids.append(new_uuid)

	def post_data(self):
		#self.channel.post_rfsensit()
		self.channel.post()
