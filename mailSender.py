from dotenv import load_dotenv
from email.message import EmailMessage
import time
import requests
import smtplib
import os
import sys
import ssl

from daemon2 import Daemon
from logger import Logger

load_dotenv()
EMISOR_EMAIL = os.getenv("EMISOR_EMAIL")
CONTRASENA = os.getenv("CONTRASENA")
URL_DEL_SERVER = os.getenv("URL_DEL_SERVER")
RECEPTOR_EMAIL = os.getenv("RECEPTOR_EMAIL")
logger = Logger("log.txt")

#Nuestro objetivo es que processId != SessionId

# 1. `Parent`    = PID: 28084, PGID: 28084, SID: 28046 -----> tenemos un padre que es lider de grupo
# 2. `Fork#1`    = PID: 28085, PGID: 28084, SID: 28046 -----> tenemos al hijo que no es lider de grupo, pero esta vinculado a una terminal existente
# 3. `Decouple#1`= PID: 28085, PGID: 28085, SID: 28085 -----> desasociamos al hijo de la terminal, haciendolo lider de una nueva sesion
# 4. `Fork#2`    = PID: 28086, PGID: 28085, SID: 28085 -----> creamos un nuevo proceso que no es lider de grupo ni sesion, ni esta vinculado a ninguna terminal



def checkear_server():
    try:
        response = requests.get(URL_DEL_SERVER)
        return response.status_code 
    except requests.ConnectionError:
        return False

def enviar_email(asunto, mensaje):

    try:

        asunto = asunto
        body = mensaje

        em = EmailMessage()
        em['From'] = EMISOR_EMAIL
        em['To'] = RECEPTOR_EMAIL
        em['asunto'] = asunto
        em.set_content(body)

        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smpt:
            smpt.login(EMISOR_EMAIL, CONTRASENA)
            smpt.sendmail(EMISOR_EMAIL, RECEPTOR_EMAIL, em.as_string())
        
        print("Correo electrónico enviado con éxito.")
    except Exception as e:
        print("Error al enviar el correo electrónico:", str(e))
    


    

def main():
    while True:
        codigo = checkear_server()
        print(codigo)
        if (codigo != 200):
            logger.escribir('ERROR', f'SE CAYÓ EL SERVIDOR - Código: {codigo}')
            enviar_email("Alerta: Servidor no está en funcionamiento", "El servidor no está respondiendo")
        else:
            logger.escribir('200',' SERVIDOR EN FUNCIONAMIENTO')

        # Esperar 30 segundos 
        time.sleep(30)


class Daemon_Custom(Daemon):

    def run(self):
        print('Esta llamando a este no?')
        main()



if __name__ == "__main__":

    argumentos = sys.argv
    if ('--accion' in argumentos):
        try:
            index = argumentos.index('--accion')
            accion = argumentos[index + 1]
            ruta_actual = os.path.dirname(__file__)
            print('ruta_actual', ruta_actual)
            archivo_pid = os.path.join(ruta_actual, 'Proceso.pid')
            print('archivo_pid', archivo_pid)
            daemon = Daemon_Custom(archivo_pid)
            match accion:
                case 'start':
                    print('ejecutaste start')
                    daemon.start()
                case 'stop':
                    print('ejecutaste stop')
                    daemon.stop()
                case 'restart':
                    print('ejecutaste restart')
                    daemon.stop()
                    daemon.start()
                case _:
                    print('Comando no reconocido')
        except Exception as e:
            print('Tenes que especificar que accion realizar utilizando el flag --accion [start/stop/restart]')
    else:
        print('Tenes que especificar que accion realizar utilizando el flag --accion [start/stop/restart]')

        

        

    
    


    
