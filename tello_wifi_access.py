import socket
import wifi_setting # custom file

tello_ip = 'xxx.xxx.xxx.xxx'
tello_port = xxxx

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (tello_ip , tello_port)

socket.sendto('command'.encode('utf-8'),tello_address)
socket.sendto(f'ap {wifi_setting.SSID} {wifi_setting.PASSWORD}'.encode('utf-8'),tello_address)
