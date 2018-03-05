import xml.etree.ElementTree
import requests
import socket
from time import gmtime, strftime


class Channel():
	def __init__(self, api_key, name, address):
		self.settings_file = "settings.xml"
		self.api_key = api_key
		self.name = name
		self.description = address
		self.buffer = []
		self.api_post_url = None
		self.load_settings()

	def add_to_buffer(self, field, value):
		self.buffer.append({'field': str(field), 'value': value})

	def post(self):
		print("Send read data to cloud")
		data = {'api_key': self.api_key}
		for pair in self.buffer:
			data['field' + pair['field']] = pair['value']
		try:
			r = requests.post(self.api_post_url, data)
			response = r.json()
			self.buffer = []
		except requests.exceptions.ConnectionError as e:
			print('Connection Error')
			response = e
		print("\nRESPONSE #")
		print(response)
		print("\n")

	def load_settings(self):
		parsed_file = xml.etree.ElementTree.parse(self.settings_file).getroot()
		# Load thingspeak settings
		server_element = parsed_file.find('server')
		thingspeak_element = server_element.find('thingspeak')
		post_address_element = thingspeak_element.find('post_address')
		self.api_post_url = post_address_element.text

