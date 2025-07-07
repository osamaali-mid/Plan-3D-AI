# Floorplan Recognition App

A modern React application for floorplan analysis and object detection.

## Current Status

⚠️ **Python Backend Unavailable**: The Python environment in this container has corrupted core modules. The frontend application runs in demo mode with mock data.

## Quick Start

### Frontend Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`

### Features Available

- ✅ Modern React UI with TypeScript
- ✅ File upload interface
- ✅ Mock floorplan analysis (demo mode)
- ✅ Results visualization
- ✅ Responsive design with Tailwind CSS
- ❌ Python backend (requires environment fix)

## Demo Mode

Since the Python backend is currently unavailable due to environment issues, the application runs in demo mode:

- File uploads are processed with mock detection results
- Sample wall, window, and door detections are generated
- All frontend functionality is preserved

## Environment Issues

The current Python installation has missing core modules:
- `_signal` module not found
- `pip` module not found  
- `_frozen_importlib` issues

To fix the Python backend:
1. Reinstall Python in a clean environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run the backend: `python start_server.py`

## Project Structure

```
├── src/
│   ├── components/     # React components
│   ├── App.tsx        # Main application
│   └── main.tsx       # Entry point
├── app/               # Python backend (currently unavailable)
├── package.json       # Node.js dependencies
└── requirements.txt   # Python dependencies
```

## Technologies

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS
- **Backend**: FastAPI, OpenCV, TensorFlow (when available)
- **UI Components**: Radix UI, Framer Motion, Lucide React