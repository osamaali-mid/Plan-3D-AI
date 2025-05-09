import cv2
import os
import numpy as np
import random

class MockModel:
    """A mock model class to simulate Mask R-CNN without TensorFlow dependency"""
    def __init__(self):
        self.name = "MockMaskRCNN"
    
    def detect(self, images, verbose=0):
        """Mock detection method that returns synthetic detection results"""
        results = []
        for image in images:
            height, width = image.shape[:2]
            
            # Create mock detection results
            num_walls = random.randint(3, 8)
            num_windows = random.randint(2, 6)
            num_doors = random.randint(1, 4)
            
            # Total detections
            total_detections = num_walls + num_windows + num_doors
            
            # Class IDs (1: Wall, 2: Window, 3: Door)
            class_ids = np.array([1] * num_walls + [2] * num_windows + [3] * num_doors)
            
            # Scores (confidence values between 0.7 and 0.98)
            scores = np.array([random.uniform(0.7, 0.98) for _ in range(total_detections)])
            
            # Bounding boxes (y1, x1, y2, x2)
            rois = []
            for _ in range(total_detections):
                x1 = random.randint(0, width - 100)
                y1 = random.randint(0, height - 100)
                x2 = min(x1 + random.randint(50, 200), width)
                y2 = min(y1 + random.randint(50, 200), height)
                rois.append([y1, x1, y2, x2])
            rois = np.array(rois)
            
            # Masks (height, width, num_instances)
            masks = np.zeros((height, width, total_detections), dtype=np.bool_)
            for i, roi in enumerate(rois):
                y1, x1, y2, x2 = roi
                mask = np.zeros((height, width), dtype=np.bool_)
                mask[y1:y2, x1:x2] = True
                
                # Make some random patterns inside the box for more realism
                for _ in range(10):
                    rx1 = random.randint(x1, x2-10)
                    ry1 = random.randint(y1, y2-10)
                    rx2 = random.randint(rx1+5, x2)
                    ry2 = random.randint(ry1+5, y2)
                    mask[ry1:ry2, rx1:rx2] = False
                
                masks[:, :, i] = mask
            
            result = {
                'rois': rois,
                'class_ids': class_ids,
                'scores': scores,
                'masks': masks
            }
            results.append(result)
        
        return results

def load_model():
    """Load a mock model that simulates Mask R-CNN"""
    print("Loading mock detection model for floorplan recognition...")
    return MockModel()

def detect_objects(image_path, output_path, model, return_json=False):
    """
    Perform mock object detection on the preprocessed floorplan image.
    
    Args:
        image_path: Path to the preprocessed image
        output_path: Path to save the output image with visualized detections
        model: Loaded mock model
        return_json: Whether to return JSON formatted results
        
    Returns:
        If return_json is True, returns a dictionary with detection results
        Otherwise, returns None after saving the output image
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Perform detection with the mock model
    results = model.detect([image], verbose=1)
    r = results[0]

    # Create a simple visualization of the results
    output_image = image.copy()
    class_names = ['BG', 'Wall', 'Window', 'Door']
    colors = {
        1: (0, 255, 0),  # Green for walls
        2: (255, 0, 0),  # Blue for windows
        3: (0, 0, 255)   # Red for doors
    }
    
    # Draw bounding boxes and labels
    for i, class_id in enumerate(r['class_ids']):
        y1, x1, y2, x2 = r['rois'][i]
        cv2.rectangle(output_image, (x1, y1), (x2, y2), colors[class_id], 2)
        cv2.putText(output_image, class_names[class_id], (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[class_id], 2)
    
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
            mask_uint8 = (mask * 255).astype(np.uint8)
            contours, _ = cv2.findContours(
                mask_uint8, 
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
