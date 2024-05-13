# image_path = r"C:\Users\omer\Desktop\open_eyes.jpg"
import cv2
import os


def extract_eyes():
    # Load the pre-trained face and eye cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Load the image
    image_path = r"C:\Users\omer\Desktop\eyes_closed_face.jpg"  # Change this to the path of your image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output_dir = "extracted_eyes"
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Iterate over each detected face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Extract the region of interest (ROI) for the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        # Detect eyes in the face region
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

        # Variable to count the detected eyes
        eye_count = 0

        # Iterate over each detected eye
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around the eye
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            # Extract the region of interest (ROI) for the eye and display it in gray
            eye_roi_gray = roi_gray[ey:ey + eh, ex:ex + ew]
            print(eye_roi_gray)
            eye_filename = os.path.join(output_dir, f"eye_{eye_count + 1}.jpg")
            cv2.imwrite(eye_filename, eye_roi_gray)

            # Increment the eye count
            eye_count += 1

            # Display only the first two eyes

    # Destroy all OpenCV windows


extract_eyes()
cv2.destroyAllWindows()
