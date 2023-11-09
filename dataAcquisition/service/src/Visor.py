from .CamaraWeb import CamaraWeb
from .HandsDetectorMP import HandsDetector
from .FaceDetector import FaceDetector
from .SimpleSecondsCounter import SecondCounter
import cv2
import json
from datetime import datetime
import os
# import zmq

class Visor():
    def __init__(self, source=None):
        self.__camara=CamaraWeb(source)
        self.__faceFrameCount = 0
        self.__MAX_FRAMES_FACE = 60
        self.__faceDetector = FaceDetector()
        self.__handDetector = HandsDetector()
        self.__secondsCounter = SecondCounter()
        self.__dataDict = {'norm_landmarks':[]}
        self.__dictMessagesPath = ""
        # self.__socket = self.clientConnection()

        ####Test mode####
        self.__countLettersDetected = 0
        self.__countLettersNotDetected = 0

    # def clientConnection(self):
    #     context = zmq.Context()
    #     socket = context.socket(zmq.REQ)
    #     socket.connect("tcp://localhost:9800")
    #     return socket

    def getFrameFromCamera(self):
        return self.__camara.getFrame()
    
    def isFaceDetected(self):
        validated, img = self.__camara.getFrame()
        if validated:
            return self.__faceDetector.isDetected(img)
        else:     
            #Problem with frame capturing
            print('It did not possible get a frame from camera')

    # def __sendInformation(self, color, face):
    #     Data.color = color
    #     Data.face = face

    def __createDictMessages(self, path='dataAcquisition/service/test/messages/'):
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        os.makedirs(path + dt_string, exist_ok=True)
        self.__dictMessagesPath = path + dt_string + '/'

    def __writeJsonFile(self, data, count):
        with open(self.__dictMessagesPath+'message_'+str(count)+'.json', 'w') as fp:
            json.dump(data, fp)


    def start(self, trafficLightColor, face, testMode=False, writeJSON=True,verbose=False):
        #Creación de documento que contiene los puntos claves de las manos
        self.__dataDict = {'hands':[]}
        separationFlag = True
        messageFlag = True
        handsFlag = False
        messageCount = 0
        self.__createDictMessages()

        while(True):
            #Captura de imagen desde cámara
            validated, img = self.__camara.getFrame()
            if validated:
                #Detect face and update count
                if not self.__faceDetector.isDetected(img):
                    self.__faceFrameCount += 1
                else:
                    self.__faceFrameCount = self.__MAX_FRAMES_FACE

                if self.__faceFrameCount > self.__MAX_FRAMES_FACE:
                    # self.__sendInformation('red', 0)
                    trafficLightColor.value = 2
                    face.value = 0
                    if verbose:
                        print('Face did not detect. ', face.value)
                    break

                img = cv2.flip(img, 1) #Change it in case of left hand
                hand = self.__handDetector.detect(img)
                if hand == None:#Hand did not detect
                    print('Hand not found')
                    self.__countLettersNotDetected += 1
                    
                    #Start counter
                    if not self.__secondsCounter.isCounting():
                        self.__secondsCounter.startCount()

                    #Separation between words
                    if self.__secondsCounter.finished(2) and separationFlag:
                        #Write blank space in file
                        self.__dataDict['hands'].append(None)
                        separationFlag = False
                        # self.__sendInformation('yellow', 1)
                        trafficLightColor.value = 1
                        face.value  = 1

                        if verbose:
                            print('Space blank detected. ', trafficLightColor.value)

                    #The message is complete
                    if self.__secondsCounter.finished(6) and messageFlag:
                        #Pass file to LSM translation module
                        #TO DO
                        messageCount += 1
                        if writeJSON and handsFlag:
                            self.__writeJsonFile(self.__dataDict, messageCount)
                        #Create a new empty file
                        self.__dataDict = {'hands':[]}
                        messageFlag = False
                        # self.__sendInformation('red', 1)
                        trafficLightColor.value = 2 #Red, change to orange
                        face.value  = 1
                        if verbose:
                            print('Message sent it. ', trafficLightColor.value)

                        #continue

                    continue

                
                separationFlag = True
                messageFlag = True
                handsFlag = True

                self.__secondsCounter.finishCount()
                self.__countLettersDetected += 1

                #Write data hand in file
                # self.__dataDict['norm_landmarks'].append(hand.getLandmarksNormalized())
                self.__dataDict['hands'].append(hand.getAttributes())

                
                # self.__sendInformation('green', 1)
                trafficLightColor.value = 0
                face.value  = 1
                if verbose:
                    print('Spelling word: ', trafficLightColor.value)
                # break

                

            else:
                #Just for testing
                #if len(self.__dataDict['norm_landmarks']) > 0:
                # print('Final data:')
                # print(self.__dataDict['norm_landmarks'])

                #Problem with frame capturing
                print('It did not possible get a frame from camera')
                break

        # print('Hands detected:',self.__countLettersDetected)
        # print('Hands did not detect:',self.__countLettersNotDetected)

