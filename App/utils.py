
import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from .constant import MODEL, PROTOTEXT, NET

class Utils:
    def __init__(self):
        # Load model face detection
        self.faceNet = cv2.dnn.readNet(PROTOTEXT, NET)

        # Load model mask detection
        self.maskNet = load_model(MODEL)


    def pred(self, image):
        
        # Dapatkan ukuran gambar
        (h, w) = image.shape[:2]

        # Dapatkan blob pada gambar
        blob = cv2.dnn.blobFromImage(image, 1.0, (224, 224), (104.0, 177.0, 123.0))
        
        # Masukkan semua koleksi blob ke dalam network
        self.faceNet.setInput(blob)

        # Lakukan forward untuk menghitung output layer
        detections = self.faceNet.forward()
        
        # Siapkan penyimpanan untuk wajah, lokasi, dan prediksi
        faces = []
        locs = []
        preds = []

        # Cari wajah
        for i in range(0, detections.shape[2]):

            # Dapatkan nilai confidence
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                # Dapatkan lokasi bounding box 
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                # Ubah tipe data bounding box ke integer
                (x0, y0, x1, y1) = box.astype("int")


                # Dapatkan koordinat bounding box
                (x0, y0) = (max(0, x0), max(0, y0))
                (x1, y1) = (min(w-1, x1), min(h-1, y1))


                # Dapatkan lokasi bounding box pada gambar wajah
                face = image[y0:y1, x0:x1]

                # Ubah warna gambar ke RGB
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

                # Resize gambar wajah sesuai dengan model deteksi masker
                face = cv2.resize(face, (224, 224))

                # Ubah format ke numpy array
                face = img_to_array(face)

                # Sesuaikan nilai dengan model caffe
                face = preprocess_input(face)

                # Simpan gambar dan lokasi bounding box
                faces.append(face)
                locs.append((x0, y0, x1, y1))

        # Cek jika wajah ada
        if len(faces) > 0:
            # Ubah gambar wajah ke numpy array float
            faces = np.array(faces, dtype="float32")

            # Prediksi masker pada wajah
            preds = self.maskNet.predict(faces, batch_size=32)

        # Dapatkan lokasi wajah dan hasil prediksi masker
        return (locs, preds)
