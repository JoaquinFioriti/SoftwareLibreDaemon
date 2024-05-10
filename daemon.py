"""Generic linux daemon base class for python 3.x."""

import sys, os, time, atexit, signal
from logs.logger import Logger
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
    
        os.chdir('/')
        os.setsid()
        os.umask(0)

        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            logger.escribir('ERROR',' FALLO EL SEGUNDO FORK')
            sys.exit(1) 
    
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
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
            return

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
