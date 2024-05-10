## TP1-DAEMON

##  Daemon de Monitoreo de Servidores

Este repositorio posee un daemon diseñado para monitorear la disponibilidad de servidores. La función principal es realizar ping a una base de datos cada 30 segundos para verificar el estado del servidor. En caso de detectar una caída del servidor, el daemon activa un sistema de alerta que notifica al administrador a través de correo electrónico.

### Pasos para correr el script 

### Instalar dependencias

1. Ejecuta el comando en tu terminal para instalar las dependencias necesarias:
-     pip3 install -r requirements.txt
  
### Crear archivo .env

2. Crea un archivo `.env` ejecutando los siguientes comandos en tu terminal:
Esto abrirá el editor nano para que  puedas configurar el `.env`. Disponemos de un `.env.example` en el repositorio para usar como guia.

-     touch .env
-     sudo nano .env

`.env.example`

### Correr script

3.  Finalmente, para ejecutar el daemon utiliza el siguiente comando en la terminal.
-     python3 mailSender.py --accion start
3.1 Para reiniciar el daemon utiliza el siguiente comando en la terminal.
-     python3 mailSender.py --accion start restart 
3.2 Para finalizar el daemon utiliza el siguiente comando en la terminal.
-     python3 mailSender.py --accion start stop
