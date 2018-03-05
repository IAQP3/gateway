import requests
import json
import xml.etree.ElementTree

# Own modules
from channel import *

class CloudPost(object):

	def __init__(self):
		print("Init cloud connection")
 
		self.settings_file = 'settings.xml'
		self.load_settings()

		# Urls
		self.get_channel_info_url = 'https://api.thingspeak.com/channels.json?api_key=' + self.user_api_key
		self.create_channel_url = 'https://api.thingspeak.com/channels.json'
		self.api_post_url = 'https://api.thingspeak.com/update.json'

		# Variables
		self.account_info = None
		self.channels = {}

	def create_channel(self, address):
		# parsed_address = address.replace(":", "")
		data = {'api_key': self.user_api_key,  'name' : 'IAQP device: ' + address, 'description': address, 'field1' : 'Ambient Temperature', 'field2' : 'Ambient Humidity', 'field3' : 'Silver Detector', 'field4' : 'Core Temperature' }
		try:
			r = requests.post(self.create_channel_url, data)
			response = r.json()
			self.parse_channel_info(response)
			#return self.channels[address]
			
		except requests.exceptions.ConnectionError as e:
			print('Connection Error')
			response = e
		print("\nRESPONSE #")
		print(response)
		print("\n")

	def get_channel_information(self):
		try:
			r = requests.get(self.get_channel_info_url)
			response = r.json()
			if response == 0:
				print("Channel information request failed!")
				return
			else:
				print("Channel info request succesfull!")
				#self.account_info = json.loads(response)
				#self.account_info_pretty_print = json.dumps(response, indent=4, sort_keys=True)
				self.parse_channel_info(response)
				print(response)

		except requests.exceptions.ConnectionError as e:
			print('Cloud connection Error\n')
			response = e

	def parse_channel_info(self, response):
		pass
		#for iter_channel in response:
		#	if "IAQP device" in iter_channel['name']:
		#		new_channel = Channel(str(iter_channel['api_keys'][0]['api_key']), iter_channel['name'], iter_channel['description'])
		#		self.channels[iter_channel['description']] = new_channel

	def print_channel_info(self):
		if self.channel_info != None:
			print(self.account_info_pretty_print)
			print("\n")
		else:
			print("Channel info not avaible!\n")

	def load_settings(self):
		parsed_file = xml.etree.ElementTree.parse(self.settings_file).getroot()
		found_keys = parsed_file.find('api_keys')
		self.user_api_key = str(found_keys.find('user_api_key').text)
