import sys
sys.path.append('../')
import cv2
from os import remove
import numpy as np

class Hand():
    def __init__(self):
        # self.__img= np.zeros((500, 500, 3), dtype=np.uint8)
        # Just in case of CNN
        # self.__img = None
        # self.__minY=0
        # self.__minX=0
        # self.__maxX=0
        # self.__maxY=0
        # self.__alto=None
        # self.__ancho=None
        self.__imgWidth = None
        self.__imgHeight = None
        self.__landmarksNormalized = None
        self.__landmarks = None
        self.__boundingBox = None
        self.__letter = ""
        self.__confidense = None


    # def getImg(self):
    #     return self.__img
    # def getMinX(self):
    #     return self.__minX
    # def getMaxX(self):
    #     return self.__maxX
    # def getMinY(self):
    #     return self.__minY
    # def getMaxY(self):
    #     return self.__maxY
    # def getAlto(self):
    #     return self.__alto
    # def getAncho(self):
    #     return self.__ancho
    # def getCoordenadas(self):
    #     return self.__coordenadas
    def getImgWidth(self):
        return self.__imgWidth
    def getImgHeight(self):
        return self.__imgHeight
    def getLandmarksNormalized(self):
        return self.__landmarksNormalized
    def getLandmarks(self):
        return self.__landmarks
    def getBoundingBox(self):
        return self.__boundingBox
    def getLetter(self):
        return self.__letter
    def getConfidense(self):
        return self.__confidense

    def getWidthBoundingBox(self):
        # if self.__boundingBox == None:
        #     return -1
        return self.__boundingBox[3]-self.__boundingBox[1]

    def getHeightBoundingBox(self):
        if self.__boundingBox == None:
            return -1
        return self.__boundingBox[2]-self.__boundingBox[0]
    
    def getAttributes(self):
        attributes = {}
        attributes['imgWidth']= self.__imgWidth
        attributes['imgHeight'] = self.__imgHeight
        attributes['landmarksNormalized'] = self.__landmarksNormalized.tolist()
        attributes['landmarks'] = self.__landmarks.tolist()
        attributes['boundingBox'] = self.__boundingBox
        attributes['letter'] = self.__letter 
        attributes['confidense'] = self.__confidense
        return attributes
    
    def setAttributes(self, attributes):
        self.__imgWidth = attributes['imgWidth']
        self.__imgHeight = attributes['imgHeight']
        self.__landmarksNormalized = attributes['landmarksNormalized']
        self.__landmarks = attributes['landmarks']
        self.__boundingBox = attributes['boundingBox']
        self.__letter = attributes['letter']
        self.__confidense = attributes['confidense']

    ####### SETTERS
    # def setImg(self,img):
    #     self.__img=img
    # def setMinX(self, d):
    #     self.__minX = d
    # def setMinY(self, d):
    #     self.__minY = d
    # def setMaxX(self, d):
    #     self.__maxX = d
    # def setMaxY(self, d):
    #     self.__maxY = d
    # def setAlto(self,alto):
    #     self.__alto=alto
    # def setAncho(self,ancho):
    #     self.__ancho=ancho
    # def setCoordenadas(self,coordenadas):
    #     self.__coordenadas=coordenadas
    def setImgWidth(self, tmp):
        self.__imgWidth = tmp
    def setImgHeight(self, tmp):
        self.__imgHeight = tmp
    def setLandMarksNormalized(self, tmp):
        self.__landmarksNormalized = tmp
    def setLandMarks(self, tmp):
        self.__landmarks = tmp
    def setBoundingBox(self, tmp):
        self.__boundingBox = tmp
    def setLetter(self, tmp):
        self.__letter = tmp
    def setConfidense(self, tmp):
        self.__confidense = tmp
