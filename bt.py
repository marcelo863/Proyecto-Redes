#!/usr/bin/python3

import pydbus
import os

# Encender bluetooth

os.system("rfkill unblock bluetooth")

BLUEZ_SERVICE='org.bluez'
ADAPTER_PATH='/org/bluez/hci0'

#bus = pydbus.SystemBus()
#adapter = bus.get(BLUEZ_SERVICE, ADAPTER_PATH)

#print("Estado adaptador:", adapter.Powered)
#if not adapter.Powered:
#	print("Encendiendo adaptador")
#	adapter.Powered = True


# Escanear dispositivos

"""
import bluetooth

def scan():

    print("Scanning for bluetooth devices:")
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    number_of_devices = len(devices)
    print(number_of_devices,"devices found")
    for addr, name, device_class in devices:
        print("\n")
        print("Device:")
        print("Device Name: %s" % (name))
        print("Device MAC Address: %s" % (addr))
        print("Device Class: %s" % (device_class))
        print("\n")
    return
"""

#scan()

import pygatt
from binascii import hexlify

adapter = pygatt.GATTToolBackend()
#adapter = pygatt.backends.BGAPIBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

try:
    adapter.start()
    #adapter.scan()
    device = adapter.connect('A8:61:0A:21:66:19')

    device.subscribe("19b10000-e8f2-537e-4f6c-d104768a1214",
                     callback=handle_data)

    # The subscription runs on a background thread. You must stop this main
    # thread from exiting, otherwise you will not receive any messages, and
    # the program will exit. Sleeping in a while loop like this is a simple
    # solution that won't eat up unnecessary CPU, but there are many other
    # ways to handle this in more complicated program. Multi-threaded
    # programming is outside the scope of this README.
    while True:
        time.sleep(10)
finally:
    adapter.stop()

