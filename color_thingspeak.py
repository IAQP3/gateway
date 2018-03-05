#!/usr/bin/env python
import sys
import time
import requests
import xml.etree.ElementTree

#Color sensor
import Adafruit_TCS34725
import smbus
tcs = Adafruit_TCS34725.TCS34725(integration_time=Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_700MS, gain=Adafruit_TCS34725.TCS34725_GAIN_1X)


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

def load_api_key():
	parsed_file = xml.etree.ElementTree.parse('color_channel_settings.xml').getroot()
	found_keys = parsed_file.find('api_keys')
	api_key = str(found_keys.find('user_api_key').text)
	return api_key

def main():

	api_key=load_api_key()
	api_post_url = 'https://api.thingspeak.com/update.json'
	
	while(1):
		data=read_sensor()
		print("Read color sensor:\n{0}".format(data))
		
		data = {'api_key': api_key, 'field1': data['r'], 'field2': data['g'], 'field3': data['b'], 'field4': data['c'], 'field5': data['l']}
		r = requests.post(api_post_url, data)
		response = r.json()
		print("Thingspeak response:\n{0}".format(response))
		print("\nGoing to sleep!")
		time.sleep(20)


if __name__ == "__main__":
	main()

	