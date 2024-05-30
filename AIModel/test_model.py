import cv2  # openCV
import torch
import pathlib


def calc_rec_center(x_right, y_top, x_left, y_bottom):
    x_center = x_left + ((x_right - x_left) / 2)
    y_center = y_bottom + ((y_top - y_bottom) / 2)
    return (x_center, y_center)


temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
model = torch.hub.load("yolov5", 'custom',
                       path="C:\\Users\\liido\\Documents\\Degree\\thirdyear\\project\\project\\pythonProject1\\yolov5\\runs\\train\\exp4\\weights\\best.pt",
                       source="local")
picture_path = "i.jpg"
image = cv2.imread(picture_path)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_resized = cv2.resize(image_gray, (640, 640))
image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_GRAY2RGB)
results = model(image_rgb)
for eye in results.pred[0]:
    # x_right, y_top, x_left, y_bottom, confidence, category = eye.numpy()
    # print(calc_rec_center(x_right, y_top, x_left, y_bottom))
    x1, y1, x2, y2, confidence, class_pred = eye.tolist()[:6]

    # Drawing rectangle on the original image
    cv2.rectangle(image_rgb, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Displaying the image with rectangles
    cv2.imshow("Detected Objects", image_rgb)
    cv2.waitKey(0)  # Waits indefinitely for a key press to close the window
    cv2.destroyAllWindows()
