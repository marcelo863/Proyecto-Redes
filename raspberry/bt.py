#!/usr/bin/python3

import os
import signal
import pygatt
import struct
#from binascii import hexlify
import time
import mysql.connector


# Direccion MAC de Portenta
MAC_ADDRESS = '02:68:70:10:29:B6'

configDB = {
    'user': 'redes',
    'password': '123',
    'host': 'localhost',
    'database':'redesDB'
}

# Encender bluetooth

os.system("sudo rfkill unblock bluetooth")

adapter = pygatt.GATTToolBackend()
#adapter = pygatt.backends.BGAPIBackend()

# manejar ctrl + C
def handle_break(sig, frame):
    print("")
    #adapter.stop()
    print("Conexión BLE terminada")
    conn.close()
    c.close()
    print("Conexión a base de datos terminada")
    exit(1)

def connectDB():
    conn = mysql.connector.connect(**configDB)
    return conn

def insertDB(conn,cursor, detect_time, detect, detect_prob):
    cursor.execute('''
          INSERT INTO registro (hora, reconocimiento, prob_reconocimiento)
          VALUES (%s,%s,%s)
          ''',(detect_time, detect, detect_prob))

    conn.commit()
    print("")


def handle_data(handle, data):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print("Hora:", now)

    data = struct.unpack("<h", data)[0]
    #print("Datos recibidos:", data)

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
    insertDB(conn, c, now, is_person, prob)

# signal para manejar ctrl + c
signal.signal(signal.SIGINT, handle_break)

try:

    # conectar a BD
    conn = connectDB()
    if not conn.is_connected():
        print("Error en conexion de base de datos")
        exit(1)
    print("Base de datos conectada")
    c = conn.cursor()

    # adaptador bluetooth
    adapter.start()

    #adapter.scan() no sirve por temas de permisos, pero se puede usar hci0

    device = adapter.connect(MAC_ADDRESS, timeout=20.0)
    print("Dispositivo BLE conectado")


    #handle: 0x0014, char properties: 0x32, char value handle: 0x0015, uuid: 00002a6e-0000-1000-8000-00805f9b34fb

    # direccion hexadecimal de caracteristica (se conserva, porque está definida en portenta/ble_person.py)
    device.subscribe("00002a6e-0000-1000-8000-00805f9b34fb",
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
