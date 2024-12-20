import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image_path, output_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    height, width = image.shape
    new_width = 1024
    new_height = int(new_width * height / width)

    # Resize image to have a width of 1024 while maintaining aspect ratio
    resized = cv2.resize(image, (new_width, new_height))
    
    # Step 1: Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # Step 2: Threshold the image to create a binary mask
    _, mask = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)

    # Step 3: Create a blank 1024x1024 image filled with white
    final_image = np.full((1024, 1024), 255, dtype=np.uint8)

    # Step 4: Center the resized mask in the blank 1024x1024 image
    y_offset = (1024 - new_height) // 2
    x_offset = (1024 - new_width) // 2
    final_image[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = mask

    # Step 5: Save the final image
    cv2.imwrite(output_path, final_image)

    # Step 4: Visualize each step
    # steps = [
    #     ("Original Image", image),
    #     ("Gaussian Blur", blurred),
    #     ("Binary Mask (Threshold 70)", mask)
    # ]

    # for title, step_image in steps:
    #     plt.figure(figsize=(8, 8))
    #     plt.imshow(step_image, cmap='gray')
    #     plt.title(title)
    #     plt.axis('off')
    #     plt.show()


if __name__ == "__main__":
    input_path = "/mnt/data/test2.jpg"
    output_path = "/mnt/data/preprocessed_floorplan.png"
    preprocess_image(input_path, output_path)
