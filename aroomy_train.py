import os
import sys
import json
import numpy as np
import tensorflow as tf
from mrcnn import model as modellib, utils
from mrcnn.config import Config
from mrcnn import visualize
from mrcnn.model import log
import cv2
import imgaug
import imgaug.augmenters as iaa

# Disable eager execution for TensorFlow 2.x compatibility
tf.compat.v1.disable_eager_execution()

# Configuration for the Floorplan dataset
class FloorplanConfig(Config):
    NAME = "aroomy"
    NUM_CLASSES = 1 + 3  # Background + (wall, window, door)
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1  # Reduce batch size to prevent OOM
    STEPS_PER_EPOCH = 50  # Ensure full dataset coverage
    VALIDATION_STEPS = 50
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 1024
    DETECTION_MIN_CONFIDENCE = 0.7
    LEARNING_RATE = 0.0001  # Start with a lower LR to prevent divergence

# Dataset preparation class
class FloorplanDataset(utils.Dataset):
    def load_floorplan(self, dataset_dir, subset):
        """Load a subset of the Aroomy dataset."""
        # Add classes
        self.add_class("aroomy", 1, "door")
        self.add_class("aroomy", 2, "wall")
        self.add_class("aroomy", 3, "window")

        # Define path to annotations
        annotations_path = os.path.join(dataset_dir, subset, "annotations", "output_annotations.json")
        with open(annotations_path) as f:
            annotations = json.load(f)

        # Verify JSON structure
        assert "images" in annotations, "Missing 'images' key in annotations JSON."
        assert "annotations" in annotations, "Missing 'annotations' key in annotations JSON."

        # Add images
        for annotation in annotations["images"]:
            image_id = annotation["id"]
            image_path = os.path.join(dataset_dir, subset, "images", annotation["file_name"])
            height, width = annotation["height"], annotation["width"]
            self.add_image("aroomy", image_id=image_id, path=image_path, width=width, height=height, annotations=annotations)

    def load_mask(self, image_id):
        """Generate instance masks for an image."""
        image_info = self.image_info[image_id]
        annotations = image_info["annotations"]
        masks = []
        class_ids = []

        for annotation in annotations["annotations"]:
            if annotation["image_id"] == image_info["id"]:
                class_id = annotation["category_id"] + 1
                segmentation = annotation["segmentation"]
                mask = np.zeros([image_info["height"], image_info["width"]], dtype=np.uint8)
                for polygon in segmentation:
                    poly = np.array(polygon, dtype=np.int32).reshape((-1, 2))
                    cv2.fillPoly(mask, [poly], 1)
                masks.append(mask)
                class_ids.append(class_id)

        if not masks:
            masks = np.zeros([image_info["height"], image_info["width"], 0], dtype=np.uint8)
            class_ids = np.array([], dtype=np.int32)
        else:
            masks = np.stack(masks, axis=-1)

        class_ids = np.array(class_ids, dtype=np.int32)
        return masks, class_ids

# Paths and configuration
print("Setting path configuration...")
ROOT_DIR = os.path.abspath(".")  # Ensure absolute path
MODEL_DIR = os.path.abspath("mrcnn")
os.makedirs(MODEL_DIR, exist_ok=True)

# COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "coco/mask_rcnn_aroomy_0025.h5")
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "coco/best_initial_weight.h5")
DATASET_DIR = os.path.join(ROOT_DIR, "dataset")
print("Set path configuration...")

# Prepare datasets
print("Preparing dataset...")
config = FloorplanConfig()
dataset_train = FloorplanDataset()
dataset_train.load_floorplan(DATASET_DIR, "train")
dataset_train.prepare()

dataset_val = FloorplanDataset()
dataset_val.load_floorplan(DATASET_DIR, "val")
dataset_val.prepare()
print("Prepared dataset")

# Dynamically update STEPS_PER_EPOCH after dataset preparation
config.STEPS_PER_EPOCH = len(dataset_train.image_ids)
print(f"STEPS_PER_EPOCH set to: {config.STEPS_PER_EPOCH}")

# Validate dataset
print("Validating dataset...")
for image_id in dataset_train.image_ids[:5]:  # Print only first 5 for efficiency
    image = dataset_train.load_image(image_id)
    masks, class_ids = dataset_train.load_mask(image_id)
    print(f"Image {image_id}: Shape={image.shape}, Masks={masks.shape}, Classes={class_ids}")

# Create model
print("Creating model...")
model = modellib.MaskRCNN(mode="training", config=config, model_dir=MODEL_DIR)
print("Created model...")

# Load pretrained weights
if not os.path.exists(COCO_WEIGHTS_PATH):
    utils.download_trained_weights(COCO_WEIGHTS_PATH)

print("Loading weights...")
model.load_weights(COCO_WEIGHTS_PATH, by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_mask"])
print("Loaded weights")

# Data Augmentation to Reduce Overfitting
# augmentation = iaa.Sequential([
#     iaa.Fliplr(0.5),  # Flip horizontally with 50% probability
#     #iaa.Affine(rotate=(-15, 15), fit_output=True),  # Keep original size
#     iaa.GaussianBlur(sigma=(0, 1.0)),  # Slight blurring
#     iaa.Multiply((0.8, 1.2))  # Brightness variation
# ], random_order=True) 

print("\n🚀 Step 1: Training heads only...")
model.train(dataset_train, dataset_val,
            learning_rate=config.LEARNING_RATE,
            epochs=20,
            layers="all"
            )

# Save trained model
print("Training complete.")
model_path = os.path.join(MODEL_DIR, "aroomy_mask_rcnn_trained.h5")
model.keras_model.save_weights(model_path)
print(f"Model weights saved at {model_path}")