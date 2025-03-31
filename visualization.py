import os
import cv2
import json
import numpy as np
from mrcnn import model as modellib
from skimage.measure import find_contours
import matplotlib.pyplot as plt
from mrcnn.config import Config
from sklearn.metrics import accuracy_score

# Define inference configuration
class InferenceConfig(Config):
    NAME = "aroomy"
    NUM_CLASSES = 1 + 3  # Background + door, wall, window
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0.1  # Lowered threshold for debugging

# Initialize inference model
ROOT_DIR = os.path.abspath(".")
MODEL_DIR = os.path.join(ROOT_DIR, "mrcnn")
inference_config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)
trained_weights_path = os.path.join(ROOT_DIR, "mrcnn/best_weights.h5")

# Load trained weights
print(f"Loading weights from: {trained_weights_path}")
print(f"Weights file exists: {os.path.exists(trained_weights_path)}")
model.load_weights(trained_weights_path, by_name=True)
print("Loaded trained weights for inference.")

# Path to val folder
DATASET_DIR = os.path.join(ROOT_DIR, "dataset")
val_folder_path = os.path.join(DATASET_DIR, "val/images")
output_folder_path = os.path.join(DATASET_DIR, "val_results")
os.makedirs(output_folder_path, exist_ok=True)

# Class names
class_names = ["BG", "door", "wall", "window"]

# Fixed colors for each class
class_colors = {
    1: (0, 0, 255),        # Door → Blue
    2: (144, 238, 144),    # Wall → Light Green
    3: (128, 0, 128)       # Window → Purple
}

# Load ground truth annotations
annotations_file = os.path.join(DATASET_DIR, "val/annotations/output_annotations.json")
with open(annotations_file, 'r') as file:
    ground_truth_annotations = json.load(file)

# Function to overlay masks with fixed colors
def overlay_masks(image, masks, class_ids):
    """Overlay instance masks with fixed colors"""
    num_instances = masks.shape[-1]
    output_image = image.copy()

    for i in range(num_instances):
        mask = masks[:, :, i]
        class_id = class_ids[i]

        # Get fixed color for class
        color = class_colors.get(class_id, (255, 255, 255))  # Default to white if not found

        # Apply mask color
        for c in range(3):
            output_image[:, :, c] = np.where(mask == 1, color[c], output_image[:, :, c])

        # Get bounding box coordinates
        y1, x1, y2, x2 = r['rois'][i]
        cv2.rectangle(output_image, (x1, y1), (x2, y2), color, 2)
        label = class_names[class_id]
        cv2.putText(output_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return output_image

# Function to generate fabric-like JSON for each image
def generate_json(masks, class_ids, scores, rois, class_names):
    """Converts mask and detection results into a JSON structure"""
    output = {"annotations": []}
    num_instances = masks.shape[-1]
    
    for i in range(num_instances):
        mask = masks[:, :, i]
        contours = find_contours(mask, 0.5)
        polygons = []
        for contour in contours:
            contour = contour.ravel().tolist()
            polygons.append(contour)
        
        annotation = {
            "class_id": int(class_ids[i]),
            "score": float(scores[i]),
            "bounding_box": [int(rois[i][0]), int(rois[i][1]), int(rois[i][2]), int(rois[i][3])],
            "polygons": polygons
        }
        output["annotations"].append(annotation)
    
    return output

# Process all images in the val folder
for image_name in os.listdir(val_folder_path):
    image_path = os.path.join(val_folder_path, image_name)

    # Check if it's an image
    if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Skipping non-image file: {image_name}")
        continue

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image at path: {image_path}")
        continue

    # Convert to RGB for processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = model.detect([image_rgb], verbose=1)
    r = results[0]

    # Generate the fabric-like JSON for detection results
    json_data = generate_json(r['masks'], r['class_ids'], r['scores'], r['rois'], class_names)

    # Save the JSON output for the current image
    json_output_path = os.path.join(output_folder_path, f"{os.path.splitext(image_name)[0]}_results.json")
    with open(json_output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Results saved at {json_output_path}")

    # Overlay masks with fixed colors on the image
    detected_image = overlay_masks(image_rgb, r['masks'], r['class_ids'])

    # Save the detected image with overlays
    detected_image_bgr = cv2.cvtColor(detected_image, cv2.COLOR_RGB2BGR)
    image_output_path = os.path.join(output_folder_path, f"{os.path.splitext(image_name)[0]}_detected.png")
    cv2.imwrite(image_output_path, detected_image_bgr)
    print(f"Detected image saved at {image_output_path}")

    # Display the detected image using Matplotlib
    plt.figure(figsize=(12, 12))
    plt.imshow(cv2.cvtColor(detected_image_bgr, cv2.COLOR_BGR2RGB))
    plt.title(f"Detected Image: {image_name}")
    plt.axis('off')
    plt.show()

print("Processing complete for all images in the val folder.")
