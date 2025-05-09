#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the floorplan recognition API
"""

import requests
import os
import sys
import argparse
from pprint import pprint

def test_health(base_url):
    """Test the health endpoint"""
    response = requests.get(f"{base_url}/health")
    print(f"Health check status: {response.status_code}")
    if response.status_code == 200:
        print("Health check response:", response.json())
    else:
        print("Error:", response.text)

def test_floorplan_detection(base_url, image_path):
    """Test the floorplan detection endpoint"""
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return

    # Prepare the file for upload
    files = {'file': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')}
    
    # Send the request
    print(f"Uploading {image_path} to {base_url}/api/floorplan/detect")
    response = requests.post(f"{base_url}/api/floorplan/detect", files=files)
    
    # Check the response
    if response.status_code == 200:
        result = response.json()
        print("\nDetection successful!")
        print(f"Result ID: {result['id']}")
        print(f"Filename: {result['filename']}")
        print(f"Image URL: {result['image_url']}")
        
        # Print detected elements statistics
        print("\nDetected elements:")
        elements = result['elements']
        print(f"Walls: {len(elements['walls'])}")
        print(f"Windows: {len(elements['windows'])}")
        print(f"Doors: {len(elements['doors'])}")
        
        # Save full JSON to a file for reference
        with open('detection_result.json', 'w') as f:
            import json
            json.dump(result, f, indent=2)
        print("\nFull result saved to detection_result.json")
        
        # If running locally, construct the URL to view the image
        if base_url.startswith('http://localhost') or base_url.startswith('http://127.0.0.1'):
            port = base_url.split(':')[-1]
            print(f"\nView the result image at: {base_url}{result['image_url']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description='Test the floorplan recognition API')
    parser.add_argument('--url', type=str, default='http://localhost:8000', help='Base URL of the API')
    parser.add_argument('--image', type=str, help='Path to an image file to test detection')
    
    args = parser.parse_args()
    
    if args.image:
        test_floorplan_detection(args.url, args.image)
    else:
        test_health(args.url)
        print("\nUse --image argument to test the detection endpoint")

if __name__ == '__main__':
    main()
