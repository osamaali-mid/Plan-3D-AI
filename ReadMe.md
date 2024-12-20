# Floorplan 2D Sketch Detector

This project focuses on detecting windows, walls, and doors from 2D sketched floorplan images. It involves generating a dataset using labeled images from the COCO dataset, training a Mask r-cnn model, and implementing a workflow to achieve accurate detection results.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Dataset Preparation](#dataset-preparation)
- [Model Training](#model-training)
- [Usage](#usage)
- [Project Initialization](#project-initialization)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project is designed to help automate the detection of architectural elements such as windows, walls, and doors in 2D floorplan sketches. Using Mask R-CNN pretrained model, the project leverages labeled data and trains a model for robust detection performance. The key components include dataset generation, model training, and evaluation.

---

## Features

- Train a Mask R-CNN model for detecting windows, walls, and doors.
- Generate dataset using COCO-labeled images.
- Evaluate detection accuracy on sketched floorplans.
- Export model results for integration into visualization tools.
- Save the result into MySQL database

---

## Requirements

To get started, ensure you have the following dependencies installed:

- Python 3.8+
- tensorflow
- keras
- OpenCV
- NumPy
- Matplotlib
- scikit-learn

Install the required Python libraries using the following command:

```bash
pip install -r floorplan_requirements.txt
```

---

## Dataset Preparation

The dataset is a critical component for training the model. Follow these steps to prepare the dataset:

1. **Download COCO Dataset**:
   - Download the COCO dataset from the [Github Mask R-CNN repository](https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5).

2. **Extract Relevant Labels**:
   - Prepare the images to train with relevant labels such as `window`, `wall`, and `door` using Label tools like LabelMe.
3. **Extract Annotations**:
    - Generate use the labelme2coo.py
```bash
pip install pycocotools
```
```bash
labelme_json_to_dataset test1.json -o output_dataset
```
Or

```bash
python labelme2coco.py train_folder output_annotations.json
```

4. **Organize the Dataset**:
   - Ensure the dataset directory is structured as follows:
     ```
     dataset/
     ├── train/
            ├──── images/
            ├──── annotations/
     ├── val/
            ├──── images/
            ├──── annotations/
     └── test/
            ├──── images/
            ├──── annotations/
     ```

---

## Model Training

1. **Train the Model**:
   - Configure the training parameters in the script (e.g., learning rate, batch size, epochs) - model_train.py.
   - Run the training script or Train via Google Colab or AWS Instance:
```bash
python model_train.py --dataset ./dataset --epochs 50 --batch-size 16
```
2. **Save the Trained Model Dataset**:
   - Save the trained model weights for future inference:
     
---

## Usage

Once the model is trained, you can use it to detect windows, walls, and doors in 2D floorplans.

1. **Inference**:
   - Use the inference script to analyze 2D floorplan images:
     ```bash
     python app/floor.py --image ./sample_images/floorplan.png
     ```

2. **Visualize Results**:
   - The script will output the results with bounding boxes overlaid on the original image.
   - Detected images will be saved in the `outputs/` directory.
   - Detected data will be saved in MySQL database.

---

## Project Initialization

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Serenaweiyingwu/aroomy-ml.git
   cd aroomy-ml
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r floor_requirements.txt
   ```

3. **Prepare Dataset**:
   Follow the [Dataset Preparation](#dataset-preparation) steps to set up the data.

4. **Train the Model**:
   Use the [Model Training](#model-training) guide to train your model.

5. **Run Inference**:
   Follow the [Usage](#usage) section to test the model.

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

