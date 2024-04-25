from dotenv import load_dotenv
from email.message import EmailMessage
import time
import requests
import smtplib
import os
import sys
import ssl

from daemon2 import Daemon






load_dotenv()
EMISOR_EMAIL = os.getenv("EMISOR_EMAIL")
CONTRASENA = os.getenv("CONTRASENA")

URL_DEL_SERVER = "http://techiflo.com"
RECEPTOR_EMAIL = "techifloapp@gmail.com"



def checkear_server():
    try:
        response = requests.get(URL_DEL_SERVER)
        if response.status_code == 200:
            return True
        else:
            return False
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
        if checkear_server():
            print("El servidor no está en funcionamiento. Enviando correo electrónico...")
            enviar_email("Alerta: Servidor no está en funcionamiento", "El servidor no está respondiendo.")
        else:
            print("El servidor está en funcionamiento.")

        # Esperar 30 segundos antes de realizar la siguiente verificación
        time.sleep(60)


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

        

        

    
    


    
