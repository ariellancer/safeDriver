import shutil

import cv2
import os
import numpy as np
import tensorflow as tf
from PIL import Image

model = tf.keras.models.load_model('eye_state_detection_model_try1.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


def extract_eyes(pictures, name):
    output_dir = fr"C:\Users\omer\Desktop\safeDrive\AIModel\extracted_eyes{name}"
    eye_count = 0
    for filename in os.listdir(pictures):
        file_path = os.path.join(pictures, filename)
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            for (ex, ey, ew, eh) in eyes:
                eye_roi_gray = roi_gray[ey:ey + eh, ex:ex + ew]
                eye_filename = os.path.join(output_dir, f"eye_{eye_count + 1}.jpg")
                cv2.imwrite(eye_filename, eye_roi_gray)
                eye_count += 1
    return output_dir


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
                predictions = model.predict(img_array)
                predicted_class = np.argmax(predictions, axis=1)
                open_eyes += predicted_class[0]
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
    # try:
    #     # Iterate over all files in the directory
    #     for filename in os.listdir(output_dir):
    #         file_path = os.path.join(output_dir, filename)
    #         try:
    #             if os.path.isfile(file_path) or os.path.islink(file_path):
    #                 os.remove(file_path)  # Remove the file or link
    #             elif os.path.isdir(file_path):
    #                 shutil.rmtree(file_path)  # Remove the directory and its contents
    #         except Exception as e:
    #             print(f"Failed to delete {file_path}. Reason: {e}")
    # except Exception as e:
    #     print(f"Failed to list directory {output_dir}. Reason: {e}")
    if open_eyes < 7:
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