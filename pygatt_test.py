#!/usr/bin/env python
import sys
import time
import requests
import xml.etree.ElementTree as xmlTree

#Bluetooth
from gattlib import DiscoveryService, GATTRequester

#Color sensor
import Adafruit_TCS34725
import smbus
try:
	tcs = Adafruit_TCS34725.TCS34725(integration_time=Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_700MS, gain=Adafruit_TCS34725.TCS34725_GAIN_1X)
except(OSError):
	print("Color sensor not found")
	
def read_sensor():
	
	# Disable interrupts
	tcs.enable()
	tcs.set_interrupt(False)
	
	#Get values
	r, g, b, c = tcs.get_raw_data()
	color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)
	lux = Adafruit_TCS34725.calculate_lux(r, g, b)
	
	rdata={'r':r, 'g':g, 'b':b, 'c':c,'t':color_temp, 'l':lux}
	
	# Enable interrupts and put the chip back to low power sleep/disabled.
	tcs.set_interrupt(True)
	tcs.disable()
	
	return rdata

def main():
	#channel = Channel()
	#ts = Thingspeak()
	
	
	address = "D5:21:56:28:B0:AF"
	
	service = DiscoveryService("hci0")
	devices = service.discover(2)

	for address, name in devices.items():
		print("name: {}, address: {}".format(name, address))
	
	sensor = Thingy(address)
	
	sensor.connect()
	print(sensor.get_primary())
	sensor.disconnect()


class Thingy():
	def __init__(self, address):
		self.requester = GATTRequester(address, False)
		
	def connect(self):
		print("Connecting...")
		try:
			self.requester.connect(True,"random") #must use "random" addressing type instead of "public"
			print("OK!")
		except(RuntimeError):
			print("Failed")
			

	def disconnect(self):
		self.requester.disconnect()
		print("Disconnected.")
	
	def get_primary(self):
		return self.requester.discover_primary()
		
		
class Thingspeak():
	def __init__(self):
		self.channel_api_url = "https://api.thingspeak.com/channels.json"
		self.user_api_key = self.load_api_key()
	
	def create_channel(self, name):
		#add api key and channel name and send post request
		data = {'api_key': self.user_api_key,  'name' : name, 'field1' : 'Temperature', 'field2' : 'Humidity'}
		try:
			res = requests.post(self.channel_api_url, data)
		except requests.exceptions.RequestException as e:
			res = e
		
		return res
	
	def get_channels(self):
		#add api key to data and send get request
		#returns list of channels, that have dictionary of attributes
		data = {}
		data.update(api_key=self.user_api_key)
		try:
			res = requests.get(self.channel_api_url, data).json()
		except requests.exceptions.RequestException as e:
			res = e
		
		return res
		
	
	def load_api_key(self):
		root = xmlTree.parse('new_settings.xml').getroot()
		child = root.find('thingspeak')
		api_key = str(child.find('user_api_key').text)
		return api_key

class Channel():
	def __init__(self):
		self.api_key = self.load_api_key()
		self.api_url = 'https://api.thingspeak.com/update.json'
	
	def post(self, data):
		#add api key to data and send post request
		data.update(api_key=self.api_key)
		try:
			res = requests.post(self.api_url, data)
		except requests.exceptions.RequestException as e:
			res = e
		
		return res

	def load_api_key(self):
		root = xmlTree.parse('new_settings.xml').getroot()
		child = root.find('channel')
		api_key = str(child.find('api_key').text)
		return api_key
	
if __name__ == "__main__":
	main()

	
	