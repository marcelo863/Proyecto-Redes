# Proyecto-Redes

La idea es que el RPi se suscriba al Portenta, con tal de recibir los datos que este 
produzca al procesar su entorno, configurándose el primero como un nodo central de BLE, 
y el Portenta como uno periférico.

## Configuración inicial

Iniciar sesión en usuario `redes` con contraseña `123`:  
```
su - redes
```

Luego actualizar e instalar dependencias:
```
sudo apt update
sudo apt upgrade
sudo apt install git mariadb-server

python3 -m pip install pygatt "pygatt[GATTTOOL]" mysql-connector-python matplotlib
```

## Base de datos

Crear usuario (la contraseña predeterminada de root en mysql es vacía, pero puede que sea "root" en este caso):
```
sudo bash dbuser.sh
```
Crear base de datos y tabla de registros:
```
mysql -u redes -p < init.sql
```
Ver contenido de tabla:
```
bash check_db.sh
``` 

## Conexión BLE

En primer lugar, buscar los dispositivos cercanos mediante BLE:  
```
hcitool -i hci0 lescan
```

Una vez encontrado el dispositivo que tenga el nombre registrado del Portenta (PORTENTA-BLE), copiar su dirección MAC en la variable `MAC_ADRESS`, en el archivo `bt.py`, utilizando `nano bt.py`.

Al terminar, finalizar la edición con `ctrl + X` y confirmar el nombre del archivo.

<!-- Luego, ejecutar `gatttool -I`, y conectarse a dispositivo utilizando `connect [dirección MAC]`.  
Una vez conectado, hay que encontrar la dirección hexadecimal de la característica a suscribirse, ejecutando `characteristics` y buscando la última enlistada.  
Una vez encontrada, reemplazar en archivo `bt.py`. -->

Finalmente, ejecutar el siguiente comando: `python 3 bt.py`





 

fuentes:
https://github.com/pcborenstein/bluezDoc/wiki/hcitool-and-gatttool-example
