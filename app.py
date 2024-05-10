from daemon import Daemon_Custom
from logs.logger import Logger
import os
import sys


logger = Logger("logs/log.txt")


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

        

        

    
    


    
