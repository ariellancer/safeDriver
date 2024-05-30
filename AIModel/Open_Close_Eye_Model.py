
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from roboflow import Roboflow
import cv2  # openCV
import torch
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Load the model from the local yolov5 directory
model_detection = torch.hub.load("yolov5", 'custom',
                       path=r"C:\Users\omer\Desktop\safeDrive\AIModel\best.pt",
                       source="local"
                       )
model_eye_conclusion = tf.keras.models.load_model('eye_state_conclusion.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
parent_dir = fr"C:\Users\omer\Desktop\safeDrive\AIModel"

#
# rf = Roboflow(api_key="QAueR76qzFzl2quFwhWp")
# project = rf.workspace().project("eyes-model")
# model_rf = project.version(1).model

# infer on a local image


def extract_eyes(pictures, name):
    output_dir = fr"extracted_eyes{name}"
    path = os.path.join(parent_dir, output_dir)
    os.mkdir(path)
    eye_count=0
    for filename in os.listdir(pictures):
        file_path = os.path.join(pictures, filename)
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            # face_filename = os.path.join(output_dir, f"face_{face_count + 1}.jpg")
            # cv2.imwrite(face_filename, roi_gray)
            image_resized = cv2.resize(roi_gray, (640, 640))
            results = model_detection(image_resized)
            for eye in results.pred[0]:
                x1, y1, x2, y2, confidence, class_pred = eye.tolist()[:6]
                roi_img = image_resized[int(y1):int(y2), int(x1):int(x2)]
                eye_filename = os.path.join(output_dir, f"eye_{eye_count+1}.jpg")
                cv2.imwrite(eye_filename, roi_img)
                eye_count += 1
    return path


def preprocess_image(output_dir, target_size=(224, 224)):
    # Load the image
    open_eyes = 0
    for filename in os.listdir(output_dir):
        try:
            # Load the image
            file_path = os.path.join(output_dir, filename)
            with Image.open(file_path) as img:
                # Convert the image to grayscale
                img_gray = img.convert('L')
                # Resize the grayscale image
                img_gray_resized = img_gray.resize(target_size)
                # Convert the grayscale image to a numpy array
                img_array_gray = np.array(img_gray_resized)
                # Create a three-channel representation by repeating the grayscale values
                img_array = np.stack((img_array_gray,) * 3, axis=-1)
                # Add an extra dimension to make it compatible with model input
                img_array = np.expand_dims(img_array, axis=0)
                # Predict the class of the image
                predictions = model_eye_conclusion.predict(img_array)
                predicted_class = np.argmax(predictions, axis=1)
                open_eyes += predicted_class[0]
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
    for filename in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, filename))
    os.rmdir(output_dir)
    if open_eyes < 3:
        return 0
    return 1


def run(pictures, name):
    output_dir = extract_eyes(pictures, name)
    return preprocess_image(output_dir)


print(run(r"C:\Users\omer\Desktop\safeDrive\AIModel\pictures", 1))
# preprocessed_image = preprocess_image(img_path)

# Predict the class of the image
# predictions = model.predict(preprocessed_image)
# predicted_class = np.argmax(predictions, axis=1)
# print(predicted_class)