import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify
from main import predict_cricket_shot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict_shot():
    # Get the base64-encoded image from the request
    image_base64 = request.json['image']
    
    # Decode the image
    image_data = base64.b64decode(image_base64)
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)

    # Pass the image to the predict_cricket_shot function
    output_image = predict_cricket_shot(image)

    # Convert the output image to base64
    _, buffer = cv2.imencode('.jpg', output_image)
    output_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Return the base64 image in a JSON response
    return jsonify({'image': output_image_base64})

if __name__ == "__main__":
    app.run(debug=True)