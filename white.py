
import os
import cv2
import numpy as np

def create_mask_from_labels(image_path, label_path, output_path):
    # Read the original image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read image: {image_path}")
        return

    # Create a mask for the image filled with white
    mask = np.ones_like(image) * 255

    with open(label_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split()  # Split line into individual values
            # Iterate through sets of five values (class_label, x_center, y_center, width, height)
            for i in range(0, len(data), 5):
                try:
                    class_label = int(data[i])  # Assuming the class label is the first value

                    # Extract normalized bounding box coordinates
                    x_center, y_center, width, height = map(float, data[i + 1:i + 5])

                    # Calculate bounding box corners in pixel coordinates
                    img_height, img_width = image.shape[:2]
                    x_min = int((x_center - width / 2) * img_width)
                    y_min = int((y_center - height / 2) * img_height)
                    x_max = int((x_center + width / 2) * img_width)
                    y_max = int((y_center + height / 2) * img_height)

                    # Fill annotated regions with black in the mask
                    cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), (0, 0, 0), -1)
                except (ValueError, IndexError):
                    continue

    # Combine the original image with the updated mask
    result = np.where(mask == 0, image, 255)  # Set areas outside annotations to white

    # Save the resulting image
    filename = os.path.basename(image_path)
    cv2.imwrite(os.path.join(output_path, f"{os.path.splitext(filename)[0]}.jpg"), result)

# Replace these paths with your actual directory paths
image_dir = 'images'
label_dir = 'labels'
output_image_dir = 'results'

# Ensure the output directory exists, create it if not
os.makedirs(output_image_dir, exist_ok=True)

# List image files in the directory
image_files = os.listdir(image_dir)
label_files = os.listdir(label_dir)

# Process each image and its corresponding label
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    label_path = os.path.join(label_dir, image_file.replace('.jpg', '.txt'))
    create_mask_from_labels(image_path, label_path, output_image_dir)
