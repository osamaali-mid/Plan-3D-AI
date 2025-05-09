# Floorplan Recognition API

This API provides endpoints for detecting architectural elements (walls, windows, and doors) in 2D floorplan sketches using a Mask R-CNN model.

## API Endpoints

### Health Check
```
GET /health
```
Returns the status of the API.

### Floorplan Detection
```
POST /api/floorplan/detect
```
Upload and process a floorplan image.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form with a `file` field containing the image file

**Response:**
```json
{
  "id": "unique-id",
  "filename": "original-filename.jpg",
  "elements": {
    "walls": [
      {
        "type": "Wall",
        "confidence": 0.98,
        "bbox": [10, 20, 100, 200],
        "contour": [[10, 20], [10, 200], [100, 200], [100, 20]]
      }
    ],
    "windows": [...],
    "doors": [...]
  },
  "image_url": "/api/floorplan/images/unique-id_detected.jpg"
}
```

### Get Detection Result Image
```
GET /api/floorplan/results/{result_id}
```
Get the processed image showing the detection results.

**Response:**
- Content-Type: `image/jpeg`
- The image with detected objects highlighted

## Running the API

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Access the API documentation:
```
http://localhost:8000/docs
```

## Testing the API

You can use the included `test_api.py` script to test the API:

```bash
# Test the health endpoint
python test_api.py --url http://localhost:8000

# Test floorplan detection with an image
python test_api.py --url http://localhost:8000 --image /path/to/your/floorplan.jpg
```

## Client Integration

### Example: JavaScript Fetch API
```javascript
async function detectFloorplan(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:8000/api/floorplan/detect', {
    method: 'POST',
    body: formData
  });
  
  if (!response.ok) {
    throw new Error('Error detecting floorplan: ' + await response.text());
  }
  
  return await response.json();
}
```

### Example: Python Requests
```python
import requests

def detect_floorplan(image_path):
    with open(image_path, 'rb') as file:
        files = {'file': (os.path.basename(image_path), file, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/floorplan/detect', files=files)
    
    response.raise_for_status()
    return response.json()
```
