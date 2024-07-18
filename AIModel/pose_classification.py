import torch
import pathlib
import cv2
import numpy as np

# Fix pathlib to handle Windows paths
pathlib.PosixPath = pathlib.WindowsPath

# Load the YOLOv5 model
model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')

# Read and preprocess the image
img = cv2.imread(r'C:\Users\liido\Documents\Degree\thirdyear\safeDrive\AIModel\pictures\1.jpg', cv2.IMREAD_COLOR)
image_resized = cv2.resize(img, (252, 252))

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

# Convert the image to a tensor and add a batch dimension
image_tensor = torch.from_numpy(image_rgb).float().permute(2, 0, 1).unsqueeze(0)  # Shape: (1, 3, 252, 252)

# Normalize the image if required (e.g., divide by 255 if the model expects pixel values between 0 and 1)
image_tensor /= 255.0

# Remove the batch dimension and convert to NumPy array for visualization
image_np = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()

# Convert the image back to BGR for OpenCV and scale back to 0-255 range
image_bgr = cv2.cvtColor((image_np * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)

# Display the image using OpenCV
cv2.imshow('Image Tensor', image_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform inference
results = model(image_tensor)

# Print results
print(results)
