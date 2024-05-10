from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import ssl
import os

load_dotenv()
EMISOR_EMAIL = os.getenv("EMISOR_EMAIL")
CONTRASENA = os.getenv("CONTRASENA")
URL_DEL_SERVER = os.getenv("URL_DEL_SERVER")
RECEPTOR_EMAIL = os.getenv("RECEPTOR_EMAIL")


class EmailService:
    
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