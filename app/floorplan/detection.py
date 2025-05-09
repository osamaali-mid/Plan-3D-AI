import cv2
import sys
import os
import numpy as np
import tensorflow as tf

# Ensure project path is in the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from mrcnn import visualize

class FloorPlanConfig(Config):
    """
    Configuration for training on the floorplan dataset.
    """
    NAME = "floorplan"
    NUM_CLASSES = 1 + 3  # Background + 3 object classes
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 1024
    IMAGE_MAX_DIM = 1024
    DETECTION_MIN_CONFIDENCE = 0.5
    RPN_ANCHOR_SCALES = (32, 64, 128, 256, 512)  # Anchor sizes
    TRAIN_ROIS_PER_IMAGE = 200
    MAX_GT_INSTANCES = 100
    
def load_model():
    """
    Load the pre-trained Mask R-CNN model with updated TensorFlow compatibility.
    """
    config = FloorPlanConfig()

    # Create the Mask R-CNN model
    model = MaskRCNN(mode="inference", model_dir="./coco", config=config)

    # Load pre-trained weights, excluding the output layers
    weights_path = os.path.abspath("./coco/mask_rcnn_coco.h5")
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Weight file not found: {weights_path}")
    
    model.load_weights(weights_path, by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
    return model

def detect_objects(image_path, output_path, model, return_json=False):
    """
    Perform object detection on the preprocessed floorplan image.
    
    Args:
        image_path: Path to the preprocessed image
        output_path: Path to save the output image with visualized detections
        model: Loaded Mask R-CNN model
        return_json: Whether to return JSON formatted results
        
    Returns:
        If return_json is True, returns a dictionary with detection results
        Otherwise, returns None after saving the output image
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Perform detection
    results = model.detect([image], verbose=1)
    r = results[0]

    # Visualize and save the results
    class_names = ['BG', 'Wall', 'Window', 'Door']
    output_image = visualize.display_instances(
        image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
    )

    # Save the output image
    output_file_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    cv2.imwrite(output_file_path, output_image)
    print(f"Output saved to: {output_file_path}")
    
    # Return JSON-formatted results if requested
    if return_json:
        detected_objects = []
        for i, class_id in enumerate(r['class_ids']):
            # Get the class name
            class_name = class_names[class_id]
            # Get the score
            score = float(r['scores'][i])
            # Get the bounding box
            y1, x1, y2, x2 = r['rois'][i]
            # Get the mask
            mask = r['masks'][:, :, i]
            
            # Create a contour from the mask
            contours, _ = cv2.findContours(
                (mask * 255).astype(np.uint8), 
                cv2.RETR_EXTERNAL, 
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Convert contours to list of points for JSON serialization
            contour_points = []
            if contours:
                # Use the largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                contour_points = largest_contour.reshape(-1, 2).tolist()
            
            # Add object to list
            detected_objects.append({
                "type": class_name,
                "confidence": score,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "contour": contour_points
            })
        
        # Group by object type
        result = {
            "walls": [],
            "windows": [],
            "doors": []
        }
        
        for obj in detected_objects:
            if obj["type"] == "Wall":
                result["walls"].append(obj)
            elif obj["type"] == "Window":
                result["windows"].append(obj)
            elif obj["type"] == "Door":
                result["doors"].append(obj)
        
        return result
    
    return None
