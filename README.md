# REMAGrafanaDashboard
## Ubidots & ThingsBoard:

### Librerias Requeridas
Utilice el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para las librerías necesarias.
1. Request \
```pip install request```
1. Geocoder \
```pip install geocoder```
1. Paho MQTT \
```pip install paho-mqtt```
### Pasos para correr el servidor

1. Crear el "Device" en cada una de las plataformas, ya sea Ubidots o ThingsBoard. En las opciones del "Device" se encontrará un token único.
1. En cada uno de los archivos .py se debe cambiar el token por el obtenido en cada una de las plataformas.
1. Correr los archivos .py utilizando el comando, donde ```nameFile.py``` es el nombre de cada uno de los archivos correspondiente a la plataforma que se desee utilizar para cargar los datos. \
```python nameFile.py```

## Grafana:




