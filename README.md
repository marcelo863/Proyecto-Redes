# Proyecto-Redes

En primer lugar, buscar los dispositivos cercanos mediante BLE:  
`hcitool -i hci0 lescan`

Una vez encontrado el dispositivo que tenga el nombre registrado del Portenta, 
copiar su dirección MAC en el archivo `bt.py` (por ahora) para conectarse a él.

Luego, ejecutar `gatttool -I`, y conectarse a dispositivo utilizando `connect [dirección MAC]`.  
Una vez conectado, hay que encontrar la dirección hexadecimal de la característica a suscribirse.  
<!-- Hay que escoger siempre el último?? --> (al parecer siempre lo es jaja)
Una vez encontrada, reemplazar en archivo `bt.py` (por ahora)

La idea es que el RPi se suscriba al Portenta, con tal de recibir los datos que este 
produzca al procesar su entorno, configurándose el primero como un nodo central de BLE, 
y el Portenta como uno periférico.
 

fuentes:
https://github.com/pcborenstein/bluezDoc/wiki/hcitool-and-gatttool-example
