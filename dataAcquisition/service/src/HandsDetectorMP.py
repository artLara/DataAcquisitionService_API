# import cv2
import mediapipe as mp
import numpy as np
from .Hand import Hand
class HandsDetector():
    def __init__(self, confidenseMP = 0.5, offsetBoundingBox = 50):
        self.__offsetBoundingBox = offsetBoundingBox
        self.mp_hands = mp.solutions.hands
        # For static images:
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=confidenseMP)

    def get_coord_lists(self, handLadmark, image_shape):
        all_x, all_y = [], [] # store all x and y points in list
        for hnd in self.mp_hands.HandLandmark:
            all_x.append(handLadmark.landmark[hnd].x * image_shape[1])
            all_y.append(handLadmark.landmark[hnd].y * image_shape[0])

        return all_x, all_y

    def getLandmarksNorm(self,x,y,bbox):
        """
        Mueve X y Y respecto al bounding box, despues lo normaliza respecto al ancho
        y largo del bounding box
        """
        x_norm = []
        y_norm = []
        for i in range(len(x)):
            aux = (x[i] - bbox[0])/(bbox[2]-bbox[0])
            x_norm.append(aux)
            aux = (y[i] - bbox[1])/(bbox[3]-bbox[1])
            y_norm.append(aux)

        return np.asarray([x_norm+y_norm])

    def get_bbox_coordinates(self, handLadmark, image_shape):
        """
        Get bounding box coordinates for a hand landmark.
        Args:
            handLadmark: A HandLandmark object.
            image_shape: A tuple of the form (height, width).
        Returns:
            A tuple of the form (xmin, ymin, xmax, ymax).
        """
        all_x, all_y = [], [] # store all x and y points in list
        offset = self.__offsetBoundingBox
        for hnd in self.mp_hands.HandLandmark:
            all_x.append(int(handLadmark.landmark[hnd].x * image_shape[1])) # multiply x by image width
            all_y.append(int(handLadmark.landmark[hnd].y * image_shape[0])) # multiply y by image height

        return max(min(all_x)-offset,0), max(min(all_y)-offset, 0), min(max(all_x)+offset, image_shape[1]), min(max(all_y)+offset, image_shape[0]) # return as (xmin, ymin, xmax, ymax)

    def detect(self, image):
        hand = Hand()
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = self.hands.process(image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if results.multi_hand_landmarks:
            bbox = (0,0,0,0)
            # for hand_landmarks in results.multi_hand_landmarks:
            #     # print(hand_landmarks)
            #     bbox = self.get_bbox_coordinates(hand_landmarks, image.shape)
            #     self.x, self.y = self.get_coord_lists(hand_landmarks, image.shape)

            bbox = self.get_bbox_coordinates(results.multi_hand_landmarks[0], image.shape)
            x, y = self.get_coord_lists(results.multi_hand_landmarks[0], image.shape)

            hand.setImgWidth(image.shape[0])
            hand.setImgHeight(image.shape[1])
            hand.setLandMarksNormalized(self.getLandmarksNorm(x,y,bbox))
            hand.setLandMarks(np.asarray(x+y))
            hand.setBoundingBox(bbox)

            # hand.setAncho(bbox[2] - bbox[0])
            # hand.setAlto(bbox[3] - bbox[1])
            # hand.setMinX(bbox[0])
            # hand.setMinY(bbox[1])
            # hand.setMaxX(bbox[2])
            # hand.setMaxY(bbox[3])
            return hand

        return None
