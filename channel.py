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

    def post_rfsensit(self):
        print("Send read data to RF-SensIT server")

        new_time = strftime("%d/%m/%y %H:%M:%S", gmtime())
        MESSAGE = new_time + " " + self.description + " "
        for pair in self.buffer:
            if int(pair['field']) == 1 or int(pair['field']) == 4:
                MESSAGE += "T=" + str(pair['value']) + "'C "
            if int(pair['field']) == 2:
                MESSAGE += "rh=" + str(pair['value']) + " "
        MESSAGE += "T=00.00'C rh=00.00 T=00.00'C rh=00.00 T=00.00'C rh=00.00"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        MESSAGE.encode('utf8')
        print("Sending data to server, address: {0}, port: {1}, send message:".format(self.TCP_IP, self.TCP_PORT))
        print(MESSAGE)
        s.send(MESSAGE)
        # data = s.recv(self.BUFFER_SIZE)
        # print("Response from RF-SensIT")
        # print(data)
        print("\n")
        s.close()
        self.buffer = []

    def load_settings(self):
        parsed_file = xml.etree.ElementTree.parse(self.settings_file).getroot()
        # Load thingspeak settings
        server_element = parsed_file.find('server')
        thingspeak_element = server_element.find('thingspeak')
        post_address_element = thingspeak_element.find('post_address')
        self.api_post_url = post_address_element.text

        # Load RF-SensIt settings
        server_element = parsed_file.find('server')
        rfsensit_element = server_element.find('rfsensit_tcp')
        self.TCP_IP = rfsensit_element.find('post_address').text
        self.TCP_PORT = int(rfsensit_element.find('post_port').text)
        self.BUFFER_SIZE = int(rfsensit_element.find('post_buffer_size').text)

