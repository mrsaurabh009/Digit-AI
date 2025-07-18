from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import base64
import re
import cv2
import os

# Initialize Flask app
app = Flask(__name__)

# Try to load model safely
model = None
try:
    model = load_model('digit_model.h5')
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Failed to load model:", str(e))

def preprocess_image(data_url):
    encoded_data = re.sub('^data:image/.+;base64,', '', data_url)
    image_data = base64.b64decode(encoded_data)
    np_data = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image decoding failed. Check the base64 input.")
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    x, y, w, h = cv2.boundingRect(thresh)
    if w == 0 or h == 0:
        digit = np.zeros((28, 28), dtype=np.uint8)
    else:
        digit = thresh[y:y+h, x:x+w]
    digit = cv2.resize(digit, (18, 18), interpolation=cv2.INTER_AREA)
    padded = np.pad(digit, ((5, 5), (5, 5)), mode='constant', constant_values=0)
    padded = padded / 255.0
    return padded.reshape(1, 28, 28, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please contact administrator.'}), 500

    try:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({'error': 'No image data received'}), 400

        processed_img = preprocess_image(image_data)
        predictions = model.predict(processed_img)
        predicted_digit = int(np.argmax(predictions))
        return jsonify({'prediction': predicted_digit})
    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({'error': str(e)}), 500

# Required for Render to detect port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 App running on port {port}")
    app.run(host='0.0.0.0', port=port)
