#!/usr/bin/python3
# fuente: https://github.com/peplin/pygatt

import os
import signal
import pygatt
import struct
from binascii import hexlify
import time
# pip install mysql-connector-python
import mysql.connector

# Encender bluetooth

os.system("sudo rfkill unblock bluetooth")


adapter = pygatt.GATTToolBackend()
#adapter = pygatt.backends.BGAPIBackend()

# manejar ctrl + C
def handle_break():
    conn.close()
    exit(1)

def connectDB():
    host_name = "localhost"
    conn = mysql.connector.connect("redes", "123", host_name, "redesDB")
    return conn

def insertDB(cursor, detect_time, detect, detect_prob):
    cursor.execute('''
          INSERT INTO registro (hora, reconocimiento, prob_reconocimiento)
            VALUES
            (%s,%d,%f),
          ''', [detect_time, detect, detect_prob])

    # imprimir resultado de query
    print(cursor.fetchall())
    cursor.commit()


def handle_data(handle, data):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print("tiempo:", now)

    data = struct.unpack("<h", data)[0]
    print("Datos recibidos:", data)

    is_person = 0
    if data > 1000:
        print("Persona detectada")
        is_person = 1
        data -= 10000

    # Extraer probabilidad
    prob = data/1000.0

    if is_person == 1:
        print("Con probabilidad", prob)

    # Ingresar datos en BD
    insertDB(c, now, is_person, prob)

# signal para manejar ctrl + c
signal.signal(signal.SIGINT, handle_break)

try:

    # conectar a mysql en docker container
    conn = connectDB()
    if not conn.is_connected():
        print("Error en conexion de base de datos")
        exit(1)
    print("Base de datos conectada")
    c = conn.cursor()

    # adaptador bluetooth
    adapter.start()

    # al parecer scan no funciona por requerir permisos especiales o algo asi.
    # Al cabo que ni lo necesitabamos >:(
    # mejor usar hci
    # adapter.scan() 

    device = adapter.connect('02:68:70:10:29:B6')
    print("Dispositivo BLE conectado")

    """
    00002a00-0000-1000-8000-00805f9b34fb
    handle: 0x000d, char properties: 0x02, char value handle: 0x000e, uuid: 00002a01-0000-1000-8000-00805f9b34fb
    handle: 0x0010, char properties: 0x20, char value handle: 0x0011, uuid: 00002a05-0000-1000-8000-00805f9b34fb
    handle: 0x0014, char properties: 0x32, char value handle: 0x0015, uuid: 00002a6e-0000-1000-8000-00805f9b34fb
    """

    # direccion hexadecimal de caracteristica
    device.subscribe("00002a6e-0000-1000-8000-00805f9b34fb",
                     callback=handle_data)
    print("Caracteristica suscrita con exito")

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

