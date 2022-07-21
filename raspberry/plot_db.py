#!/usr/bin/python3

"""
sudo apt install libjpeg-dev zlib1g-dev
python3 -m pip install Cython Pillow
python3 -m pip install matplotlib
"""

import matplotlib
from datetime import datetime
# import pytz
import matplotlib.pyplot as plt
import mysql.connector

# Direccion MAC de Portenta
MAC_ADDRESS = '02:68:70:10:29:B6'

configDB = {
    'user': 'redes',
    'password': '123',
    'host': 'localhost',
    'database':'redesDB'
}


# conectar a BD
conn = mysql.connector.connect(**configDB)

if not conn.is_connected():
    print("Error en conexion de base de datos")
    exit(1)

print("Base de datos conectada")
c = conn.cursor()

c.execute("SELECT hora, reconocimiento, prob_reconocimiento FROM registro;")
result = c.fetchall

hora_pers = []
rec_pers = []
prob_pers = []

hora_non = []
rec_non = []
prob_non = []

for i in c:
    
    # datos en reconocimiento
    if i[1]:
        hora_pers.append(i[0])
        prob_pers.append(i[2])
    
    # datos en non reconocimiento
    else:
        hora_non.append(i[0])
        prob_non.append(i[2])


print("horas_pers:", hora_pers)
print("probs_pers:", prob_pers)
print("horas_non:", hora_non)
print("probs_non:", prob_non)


# hora_pers = ["2022-07-20 05:23:54", "2022-07-20 05:23:58", "2022-07-20 05:24:09"]
# prob_pers = [0.945, 0.944, 0.957]
# hora_non = ["2022-07-20 05:24:21", "2022-07-20 07:22:24"]
# prob_non = [0.542, 0.453]

fig = plt.figure()
ax = fig.add_subplot(111)
f_non = ax.bar(hora_non, prob_non, width=0.1, label="f_non")
f_pers = ax.bar(hora_pers, prob_pers, width=0.1, label="f_pers")

# test = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M') 
# ax.xaxis.axis_date(pytz.timezone('US/Eastern').localize(test))

# plt.gca().xaxis.axis_date()

ax.set_xlabel("Hora")
ax.set_ylabel("Probabilidad de reconocimiento")
ax.set_title("Reconocimiento de personas")

ax.legend(handles=[f_non, f_pers], loc="best")

plt.xticks(rotation = 20)
# plt.margins()
# plt.show()

plt.savefig('prob_person.png')
