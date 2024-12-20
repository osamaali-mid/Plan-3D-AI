import os
import requests

def download_pretrained_model(model_dir="./models/mask_rcnn/"):
    """
    Download pre-trained Mask R-CNN model weights if not already present.
    """
    url = "https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "mask_rcnn_coco.h5")
    
    if not os.path.exists(model_path):
        print("Downloading pre-trained Mask R-CNN weights...")
        response = requests.get(url, stream=True)
        with open(model_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Model downloaded to {model_path}")
    else:
        print("Pre-trained model weights already exist.")

if __name__ == "__main__":
    download_pretrained_model()
