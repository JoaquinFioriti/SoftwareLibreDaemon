"""Generic linux daemon base class for python 3.x."""

import sys, os, time, atexit, signal
from logger import Logger
logger = Logger("log.txt")

class Daemon:
    """A generic daemon class.
    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile): 
        self.pidfile = pidfile
    
    def daemonize(self):
        
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            logger.escribir('ERROR',' FALLO EL PRIMER FORK')
            sys.exit(1)
    
        os.chdir('/')  #Asiganmos el proceso al directorio base
        os.setsid()  #Desasociamos el subproceso de la terminal inicial y lo volvemos lider de proceso y de terminal
        os.umask(0) #Le damos los permisos de escritura y lectura de archivos al demonio
    
        # segundo fork
        #De esta manera creamos un nuevo proceso para que el PID != SESSID y no tenga acceso una terminal en un futuro
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            logger.escribir('ERROR',' FALLO EL SEGUNDO FORK')
            sys.exit(1) 
    
        # Limpiamos los buffers
        sys.stdout.flush()
        sys.stderr.flush()

        # Abimos las referencias a los descriptores para posterior clonacion 
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        # Clonamos que los descirptores de nuestro proceso sean igual que los descriptores devnull. Que descarte todo
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # registramos la funcion delpid para que se ejecute al finalizar el proceso
        atexit.register(self.delpid)

        # creo archivo con el pidfile
        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):

        #Checkear en el archivo pid para ver si el demonio ya esta corriendo
        try:
            with open(self.pidfile,'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile {0} already exist. " + \
                    "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            logger.escribir('ERROR',' EL DAEMON YA SE ENCUENTRA CORRIENDO')
            sys.exit(1)
        
        logger.escribir('START','INICIAMOS DAEMON')
        self.daemonize()
        self.run()

    def stop(self):

        # Get the pid from the pidfile
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile {0} does not exist. " + \
                    "Daemon not running?\n"
            logger.escribir('ERROR',' SE INTENTO DETENER DAEMON NO EXISTENTE')
            sys.stderr.write(message.format(self.pidfile))
            return # not an error in a restart

        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                logger.escribir('END','FINALIZAMOS DAEMON')
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print (str(err.args))
                sys.exit(1)

    def restart(self):
        logger.escribir('RESTART','REINICIAMOS DAEMON')
        self.stop()
        self.start()

    def run(self):
        print('O esta llamando al viejo?')