from daemon import Daemon
from logs.logger import Logger
from dotenv import load_dotenv
from email.message import EmailMessage
import time
import requests
import smtplib
import os
import sys
import ssl

load_dotenv()
EMISOR_EMAIL = os.getenv("EMISOR_EMAIL")
CONTRASENA = os.getenv("CONTRASENA")
URL_DEL_SERVER = os.getenv("URL_DEL_SERVER")
RECEPTOR_EMAIL = os.getenv("RECEPTOR_EMAIL")
logger = Logger("logs/log.txt")

def checkear_server():
    try:
        response = requests.get(URL_DEL_SERVER)
        return response.status_code 
    except requests.ConnectionError:
        return 500

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
        if (codigo != 200):
            texto = f" SE CAYO EL SERVIDOR - CODIGO: {codigo} \n"
            logger.escribir('ERROR', texto)
            enviar_email("Alerta: Servidor no está en funcionamiento", "El servidor no está respondiendo")
        else:
            logger.escribir('200',' SERVIDOR EN FUNCIONAMIENTO')

        time.sleep(30)


class Daemon_Custom(Daemon):

    def run(self):
        main()



if __name__ == "__main__":

    argumentos = sys.argv
    if ('--accion' in argumentos):
        try:
            index = argumentos.index('--accion')
            accion = argumentos[index + 1]
            ruta_actual = os.path.dirname(__file__)
            archivo_pid = os.path.join(ruta_actual, 'Proceso.pid')
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

        

        

    
    


    
