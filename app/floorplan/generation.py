import cv2
import numpy as np

def generate_image(detected_image_path, output_path):
    """
    Generate a new image with distinct colors for walls, windows, and doors.

    :param detected_image_path: Path to the detected image
    :param output_path: Path to save the generated image
    """
    # Load detected image
    image = cv2.imread(detected_image_path)
    
    # Define colors for walls, windows, and doors
    wall_color = [0, 255, 0]   # Green
    window_color = [255, 0, 0] # Blue
    door_color = [0, 0, 255]   # Red

    # Mock masks for example
    mask = np.zeros_like(image)
    mask[:, :, 0] = image[:, :, 0]
    colored_image = cv2.addWeighted(image, 0.7, mask, 0.3, 0)

    # Save the final image
    cv2.imwrite(output_path, colored_image)

if __name__ == "__main__":
    input_path = "../../data/output/detected_output.jpg"
    output_path = "../../data/output/generated_image.jpg"
    generate_image(input_path, output_path)
