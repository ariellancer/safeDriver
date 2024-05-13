import numpy as np
import tensorflow as tf
from PIL import Image

# Load the trained model
model = tf.keras.models.load_model('face_eyes_state_detection_model.h5')


# Define a function to predict eye state from an image
def predict_eye_state(image_path):
    # Load and preprocess the image
    img = Image.open(image_path).resize((100, 100)).convert("RGB")  # Resize the image to match the model input size
    img_array = np.array(img)  # Convert the image to numpy array
    img_array = img_array / 255.0  # Normalize pixel values to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict eye state
    prediction = model.predict(img_array)
    print(prediction[0][0])
    # If prediction is close to 0, classify as closed eye; if close to 1, classify as open eye
    if prediction < 0.5:
        return "Closed"
    else:
        return "Open"


# Path to the eye image
image_path = r"C:\Users\omer\Desktop\try1_closed.jpg"

# Predict the eye state
predicted_state = predict_eye_state(image_path)
print(predicted_state)
