from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
from rembg import remove
import os
from io import BytesIO

app = Flask(__name__)

# Ensure processed images directory exists
os.makedirs("processed_images", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    file = request.files['image']
    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

    # Remove background
    processed = remove(image)

    # Convert background to white
    if processed.shape[2] == 4:  # If it has alpha channel
        alpha = processed[:, :, 3] / 255.0
        white_bg = np.ones_like(processed[:, :, :3]) * 255
        processed = (1. - alpha[:, :, None]) * white_bg + alpha[:, :, None] * processed[:, :, :3]
        processed = processed.astype(np.uint8)

    # Enhance image quality
    processed = cv2.detailEnhance(processed, sigma_s=10, sigma_r=0.15)

    # Save processed image
    processed_path = os.path.join("processed_images", "output.png")
    cv2.imwrite(processed_path, processed)

    return send_file(processed_path, mimetype='image/png')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Get PORT from Render, default to 10000
    app.run(host='0.0.0.0', port=port, debug=True)

