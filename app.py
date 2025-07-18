from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import base64
import re
import cv2
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'digit_model_fixed.h5'

try:
    model = load_model(MODEL_PATH)
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Failed to load model: {str(e)}")
    model = None

def preprocess_image(data_url):
    try:
        # Remove the base64 header
        encoded_data = re.sub('^data:image/.+;base64,', '', data_url)
        image_data = base64.b64decode(encoded_data)
        np_data = np.frombuffer(image_data, np.uint8)

        # Decode image
        img = cv2.imdecode(np_data, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Image decoding failed. Check base64 input.")

        # Invert and threshold
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # Find bounding box
        x, y, w, h = cv2.boundingRect(thresh)
        if w == 0 or h == 0:
            digit = np.zeros((28, 28), dtype=np.uint8)
        else:
            digit = thresh[y:y+h, x:x+w]

        # Resize and pad to 28x28
        digit = cv2.resize(digit, (18, 18), interpolation=cv2.INTER_AREA)
        padded = np.pad(digit, ((5, 5), (5, 5)), mode='constant', constant_values=0)

        # Normalize and reshape
        padded = padded / 255.0
        padded = padded.reshape(1, 28, 28, 1)

        return padded
    except Exception as e:
        raise ValueError(f"Error during image preprocessing: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'})

    try:
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({'error': 'No image data received'})

        processed_img = preprocess_image(image_data)
        predictions = model.predict(processed_img)
        predicted_digit = int(np.argmax(predictions))

        return jsonify({'prediction': predicted_digit})
    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
