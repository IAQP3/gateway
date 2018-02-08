#!/usr/bin/env python
import sys
import time

# Own modules
from cloudpost import *
from devices import *
from device import *
from channel import *

def main():

    
    # Urls
    create_channel_url = 'https://api.thingspeak.com/channels.json' 
    api_post_url = 'https://api.thingspeak.com/update.json'
    
    # Api Keys
    #user_api_key = '...'
    #iaqp_api_key = '...'

    cloud = CloudPost()
    devices = BlueDevices()
    
    devices_list = []
    used_addresses = []
    device = None
    status = False

    cloud.get_channel_information()

    try:
        while True:
            devices.search_BLE()
            found_devices = devices.get_iaqp_device()
            if len(found_devices) != 0:
                for dev in found_devices:
                    if dev not in used_addresses:
                        device = Device(dev)
                        device.connect()
                        if cloud.channels.get(device.address) != None:
                            device.init_channel(cloud.channels[device.address])
                        else:
                            new_channel = cloud.create_channel(device.address)
                            device.init_channel(new_channel)
                        device.load_characteristics()
                        devices_list.append(device)
                        used_addresses.append(dev['address'])
            else:
                print("Could not find any iaqp devices")

            for device in devices_list:
                device.check_connection()
                if not device.status:
                    device.reconnect()
            
            if devices_list != None:
                data = None
                for device in devices_list:
                    if device.status:
                        device.request_data() 
                    device.post_data()
            time.sleep(15)
    except KeyboardInterrupt:
        if len(devices_list) != 0:
            for device in devices_list:
                device.disconnect()
#cloud.post_data(data)

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

if __name__ == "__main__":
    main()
