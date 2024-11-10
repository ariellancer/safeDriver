import time
import os
import numpy as np
import tensorflow as tf
import cv2
import torch
import pathlib
import concurrent.futures
from threading import Lock

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model_detection = torch.hub.load("../AIModel/yolov5", 'custom',
                                 path="../AIModel/eyes_detection_model.pt",
                                 source="local"
                                 )
model_eye_conclusion = tf.keras.models.load_model('../AIModel/eye_state_conclusion.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect(pictures):
    def process_image(file_path):
        nonlocal open_eyes
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        local_open_eyes = 0
        try:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                image_resized = cv2.resize(roi_gray, (640, 640))
                results = model_detection(image_resized)
                for eye in results.pred[0]:
                    x1, y1, x2, y2, confidence, class_pred = eye.tolist()[:6]
                    img_gray = image_resized[int(y1):int(y2), int(x1):int(x2)]
                    img_gray_resized = cv2.resize(img_gray, (224, 224))
                    img_array = np.stack((img_gray_resized,) * 3, axis=-1)
                    img_array = np.expand_dims(img_array, axis=0)
                    predictions = model_eye_conclusion.predict(img_array)
                    predicted_class = np.argmax(predictions, axis=1)
                    local_open_eyes += predicted_class[0]
            with lock:
                open_eyes += local_open_eyes

        except Exception as e:
            pass

    open_eyes = 0
    lock = Lock()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(pictures):
            file_path1 = os.path.join(pictures, filename)
            futures.append(executor.submit(process_image, file_path1))

        for future in concurrent.futures.as_completed(futures):
            future.result()  # wait for all threads to complete
    if open_eyes < 1:
        return 0
    return 1