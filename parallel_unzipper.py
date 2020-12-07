import multiprocessing as mp
import threading
import argparse
import zipfile
import pathlib
import logging
import socket
import queue
import time
import os

CPU_THREADS = mp.cpu_count()
STOP_PROGRAM = False
EXIT_SERVER_PORT = 8999

logging.basicConfig(filemode='a',level=logging.INFO,filename=r"D:\development\src\python-projects\test\parallel_unzipper\parallel_unzipper.log",format='%(asctime)s unzipper [%(levelname)s] %(message)s',datefmt='%a %d %m %Y %H:%M:%S %z ')
logger = logging.getLogger(__name__)
q = queue.Queue(maxsize=0)
LOCK = threading.Lock()


def task(filename):
    pass

class UnzipperThread(threading.Thread):
    def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q

class PopulaterThread(threading.Thread):
    def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
    
    def run(self):
        global STOP_PROGRAM
        while not STOP_PROGRAM and not self.q.empty():
            print(self.q.get_nowait())


class CheckForStopProgram(threading.Thread):
    def run(self):
        global STOP_PROGRAM
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("localhost",EXIT_SERVER_PORT))
        server.listen()
        logging.info("Started exit server")
        logging.debug("Started server " + str(server))
        while True:
            client,addr = server.accept()
            with client:
                client.sendall(b"command:")
                logging.debug("Connected from " + str(addr))
                response = str(client.recv(1024).decode().rstrip('\n'))
                print(response)
                if(response == "EXIT"):
                    client.send(b"ACK")
                    STOP_PROGRAM = True
                    logging.info("Stop server received from " + str(addr))
                    break
                client.sendall(b"Sorry")
            


if __name__ == "__main__":
    
    mp.freeze_support()
    mp.set_start_method('spawn')
    logging.info("Started unzipper")
    #parser = argparse.ArgumentParser(description='Unzips all zip files in given locations in command line')
    #parser.add_argument('locations', metavar='location', nargs='+', type=str, help='the location to look for zip files')
    #args = parser.parse_args()
    #for location in args.locations:
    #    if os.path.exists(location) and os.path.isdir(location):
    #        pass
    #    else:
    #        logger.warning(location + " is not valid directory. Skipping it")
    #        args.locations.remove(location)
    
    #print(args.locations)
    

    populatorthread = PopulaterThread(1,"PT1",q)
    populatorthread.start()
    server = CheckForStopProgram()
    server.start()


    print("Hello: " + str(server.is_alive()))
    
    populatorthread.join()
    server.join()
    logging.info("End of unzipper")
