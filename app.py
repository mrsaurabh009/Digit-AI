
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import base64
import re
import cv2

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = load_model('digit_model.h5')

def preprocess_image(data_url):
    # Remove the base64 header
    encoded_data = re.sub('^data:image/.+;base64,', '', data_url)
    image_data = base64.b64decode(encoded_data)
    np_data = np.frombuffer(image_data, np.uint8)

    # Convert to grayscale image
    img = cv2.imdecode(np_data, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image decoding failed. Check the base64 input.")

    # Invert image to make digits white on black
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Crop digit region
    x, y, w, h = cv2.boundingRect(thresh)
    if w == 0 or h == 0:
        digit = np.zeros((28, 28), dtype=np.uint8)
    else:
        digit = thresh[y:y+h, x:x+w]

    # Resize to 18x18 and pad to 28x28
    digit = cv2.resize(digit, (18, 18), interpolation=cv2.INTER_AREA)
    padded = np.pad(digit, ((5, 5), (5, 5)), mode='constant', constant_values=0)

    # Normalize and reshape
    padded = padded / 255.0
    padded = padded.reshape(1, 28, 28, 1)

    return padded

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
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
    app.run(debug=True)
