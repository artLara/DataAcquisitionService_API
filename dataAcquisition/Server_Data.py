import zmq    
from .service.src.data import Data

class DataAcquisition():
    def __init__(self):
        context = zmq.Context()
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind("tcp://127.0.0.1:9800")

    def listing(self):
        print('Server listening from: tcp://127.0.0.1:9800')
        while True:
            #  Wait for next request from client
            print('Esperando mensajitoooo')
            message = self.__socket.recv()
            print("Received request: %s" % message)
            message = message.tostring().split()
            Data.color = message[0]
            Data.face = int(message[1])
            print("Received request: %s" % message)
            self.__socket.send(b"Recived")
