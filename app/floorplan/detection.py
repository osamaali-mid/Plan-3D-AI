import cv2
import sys
import os
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

def detect_objects(image_path, output_path, model):
    """
    Perform object detection on the preprocessed floorplan image.
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
