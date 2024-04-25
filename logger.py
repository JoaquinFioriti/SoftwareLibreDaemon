from datetime import datetime

class  Logger:
    def __init__(self, archivo):
        self.archivo = archivo
    
    def escribir(self, status, texto):
        try:
            with open(self.archivo, 'a') as archivo:
                hora  = datetime.now().strftime(" %Y-%m-%d %H:%M:%S ")
                # Combinar el texto con la fecha y hora
                texto_hora = f"[{status}] - [ {hora}] - {texto} \n"
                archivo.write( texto_hora)
            print("Escribimos en el logger", texto)
        except Exception as e:
            print("Error al escribir en el archivo:", e)