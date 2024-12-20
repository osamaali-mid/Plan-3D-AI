import sys
import os

# Add Mask_RCNN to system path for imports
sys.path.append(os.path.abspath("Mask_RCNN"))

from floorplan.preprocess import preprocess_image
from floorplan.detection import load_model, detect_objects
from floorplan.generation import generate_image
from floorplan.utils import create_directory


def main():
    # Directory paths
    raw_image_path = "./data/raw/test2.jpg"
    processed_image_path = "./data/processed/preprocessed_image.png"
    detected_output_path = "./data/output/detected_output.jpg"
    generated_image_path = "./data/output/generated_image.jpg"

    print(f"Looking for image at: {os.path.abspath(raw_image_path)}")
    if not os.path.exists(raw_image_path):
        raise FileNotFoundError(f"Image file not found: {raw_image_path}")
    # Ensure directories exist
    create_directory("./data/processed/")
    create_directory("./data/output/")

    # Step 1: Preprocess the raw image
    # print("Preprocessing the image...")
    preprocess_image(raw_image_path, processed_image_path)
    # print("Preprocessed the image...")

    # Step 2: Perform object detection
    print("Detecting objects in the image...")
    model = load_model()  # Load the Mask R-CNN model
    detect_objects(processed_image_path, detected_output_path, model)

    # Step 3: Generate the final image
    #print("Generating the final image...")
    #generate_image(detected_output_path, generated_image_path)

    #print("Pipeline complete! Results are saved in ./data/output/")


if __name__ == "__main__":
    main()
