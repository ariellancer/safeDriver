import time
import os
import numpy as np
import tensorflow as tf
import cv2
import torch
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model_detection = torch.hub.load("yolov5", 'custom',
                                 path="eyes_detection_model.pt",
                                 source="local"
                                 )
model_eye_conclusion = tf.keras.models.load_model('eye_state_conclusion.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect(pictures):
    eye_count = 0
    open_eyes = 0

    for filename in os.listdir(pictures):
        file_path = os.path.join(pictures, filename)
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
                open_eyes += predicted_class[0]
                eye_count += 1
    if open_eyes < 3:
        return 0
    return 1


result = 0
times = 10
start_time = time.time()
for i in range(times):
    result += detect("pictures")
end_time = time.time()
print(f"Result: {result}")
print(f"Elapsed time: {(end_time - start_time)/ times} seconds")

