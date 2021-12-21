
import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from .constant import MODEL, PROTOTEXT, NET

class Utils:
    def __init__(self):
        self.faceNet = cv2.dnn.readNet(PROTOTEXT, NET)
        self.maskNet = load_model(MODEL)


    def pred(self, frame):
        
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        
        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()
        
        faces = []
        locs = []
        preds = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x0, y0, x1, y1) = box.astype("int")

                (x0, y0) = (max(0, x0), max(0, y0))
                (x1, y1) = (min(w-1, x1), min(h-1, y1))

                face = frame[y0:y1, x0:x1]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

                faces.append(face)
                locs.append((x0, y0, x1, y1))

        if len(faces) > 0:
            faces = np.array(faces, dtype="float32")
            preds = self.maskNet.predict(faces, batch_size=32)

        return (locs, preds)
