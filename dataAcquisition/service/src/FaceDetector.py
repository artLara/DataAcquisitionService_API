import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# import inspect
# import os

class FaceDetector():
    def __init__(self, source=None):
        self.__detector = self.__initializeDetector()

    def __initializeDetector(self):
        
        # dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        # filename = os.path.join(dirname, 'relative/path/to/file/you/want')
        base_options = python.BaseOptions(model_asset_path='../bin/detector.tflite')
        options = vision.FaceDetectorOptions(base_options=base_options)
        detector = vision.FaceDetector.create_from_options(options)
        return detector
    
    def isDetected(self, image):
        rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        detection_result = self.__detector.detect(rgb_frame)
        return len(detection_result.detections) > 0