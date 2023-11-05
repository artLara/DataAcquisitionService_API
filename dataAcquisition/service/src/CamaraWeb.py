import cv2

class CamaraWeb():
    def __init__(self, source=None):
        if source == None:
            self.__cap = cv2.VideoCapture(2)
        else:
            self.__cap = cv2.VideoCapture(source)

    def setSource(self, source):
        self.__cap = cv2.VideoCapture(source)

    def getFrame(self):
        # return cv2.flip(img, 1)
        return self.__cap.read()

    def desconectar(self):
        self.__cap.release()
