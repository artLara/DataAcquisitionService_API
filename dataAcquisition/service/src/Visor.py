from CamaraWeb import CamaraWeb
from HandsDetectorMP import HandsDetector
from FaceDetector import FaceDetector
from SimpleSecondsCounter import SecondCounter
import cv2

class Visor():
    def __init__(self, source=None):
        self.__camara=CamaraWeb(source)
        self.__faceFrameCount = 0
        self.__MAX_FRAMES_FACE = 60
        self.__faceDetector = FaceDetector()
        self.__handDetector = HandsDetector()
        self.__secondsCounter = SecondCounter()
        self.__dataDict = {'norm_landmarks':[]}

        ####Test mode####
        self.__countLettersDetected = 0
        self.__countLettersNotDetected = 0

    def __createJSONfile(self):
        pass

    def start(self, testMode=False, verbose=False):
        #Creación de documento que contiene los puntos claves de las manos
        self.__dataDict = {'norm_landmarks':[]}
        separationFlag = True
        messageFlag = True

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
                    if verbose:
                        print('Face did not detect')
                    break

                self.__dataDict['width'] = img.shape[0]
                self.__dataDict['height'] = img.shape[1]
                img = cv2.flip(img, 1) #Change it in case of left hand
                hand = self.__handDetector.detect(img)
                if hand == None:#Hand did not detect
                    self.__countLettersNotDetected += 1
                    
                    #Start counter
                    if not self.__secondsCounter.isCounting():
                        self.__secondsCounter.startCount()

                    #Separation between words
                    if self.__secondsCounter.finished(2) and separationFlag:
                        #Write blank space in file
                        self.__dataDict['norm_landmarks'].append(None)
                        separationFlag = False
                        if verbose:
                            print('Space blank detected')

                    #The message is complete
                    if self.__secondsCounter.finished(6) and messageFlag:
                        #Pass file to LSM translation module
                        
                        if verbose:
                            print('Message sent it')
                            print(self.__dataDict)
                        #Create a new empty file
                        self.__dataDict = {'norm_landmarks':[]}
                        messageFlag = False
                        #continue

                    continue

                if verbose:
                    print('Spelling word')
                separationFlag = True
                messageFlag = True
                self.__secondsCounter.finishCount()
                self.__countLettersDetected += 1

                #Write data hand in file
                # self.__dataDict['norm_landmarks'].append(hand.getLandmarksNormalized())
                self.__dataDict['norm_landmarks'].append('hand')
                

                

            else:
                #Just for testing
                #if len(self.__dataDict['norm_landmarks']) > 0:
                print('Final data:')
                print(self.__dataDict['norm_landmarks'])

                #Problem with frame capturing
                print('It did not possible get a frame from camera')
                break

        print('Hands detected:',self.__countLettersDetected)
        print('Hands did not detect:',self.__countLettersNotDetected)




