# import base64
# import cv2
# import numpy as np
# from flask import Flask, request, jsonify
# from main import predict_cricket_shot
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/predict', methods=['POST'])
# def predict_shot():
#     # Get the base64-encoded image from the request
#     image_base64 = request.json['image']
    
#     # Decode the image
#     image_data = base64.b64decode(image_base64)
#     image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)

#     # Pass the image to the predict_cricket_shot function
#     output_image = predict_cricket_shot(image)

#     # Convert the output image to base64
#     _, buffer = cv2.imencode('.jpg', output_image)
#     output_image_base64 = base64.b64encode(buffer).decode('utf-8')

#     # Return the base64 image in a JSON response
#     return jsonify({'image': output_image_base64})

# if __name__ == "__main__":
#     app.run(debug=True)

# import base64
# import cv2
# import numpy as np
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# # Assuming predict_cricket_shot is defined in another module
# from main import predict_cricket_shot

# app = Flask(__name__)
# CORS(app)

# @app.routeL('/')
# def home():
#     return "Welcome"

# @app.route('/Sailor/cricketFile.html', methods=['POST'])
# def predict_shot():
#     # Get the base64-encoded image from the request
#     image_base64 = request.json['image']
    
#     # Decode the image
#     image_data = base64.b64decode(image_base64)
#     nparr = np.frombuffer(image_data, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Pass the image to the predict_cricket_shot function
#     output_image = predict_cricket_shot(image)

#     # Convert the output image to base64
#     _, buffer = cv2.imencode('.jpg', output_image)
#     output_image_base64 = base64.b64encode(buffer).decode('utf-8')

#     # Return the base64 image in a JSON response
#     return jsonify({'image': output_image_base64})

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask , send_from_directory , render_template, request ,redirect, url_for
import os
import subprocess
# Create the Flask app
app = Flask(__name__,static_url_path='/assets', static_folder='Sailor/assets')

# Define a route for the home page
@app.route('/')
def home():
    return send_from_directory('Sailor', 'index.html')

@app.route('/cricket.html')
def cricket():
    return send_from_directory('Sailor', 'cricket.html')
@app.route('/Kabaddi.html')
def Kabbadi():
    return send_from_directory('Sailor', 'Kabaddi.html')
@app.route('/Football.html')
def football():
    return send_from_directory('Sailor', 'Football.html')

@app.route('/cricketFile.html',methods=['GET', 'POST'])
def cricketFile():
        if request.method == 'POST':
            print("Entering into the file submmission")
        # Check if the post request has the file part
            if 'file' not in request.files:
                print("file is not getting...")
                return redirect(request.url)
                # return redirect(request.url)
            file = request.files['file']
            print(file)
        # If user does not select file, browser also
        # submit an empty part without filename
            if file.filename == '':
                # flash('No selected file')
                print("No such file detected")
                return redirect(request.url)
            if file:
            # Change the path to your desired directory
                print("Founded the file")
                upload_folder = os.path.join(app.root_path)
                print(upload_folder)
                filename = "sample.jpg"
                file.save(os.path.join(upload_folder, filename))
            if not os.path.exists(upload_folder):
                print("Location not found")
                os.makedirs(upload_folder)
                filename = "sample.jpg"
                file.save(os.path.join(upload_folder, filename))
                # file.save(os.path.join(upload_folder, file.filename))
            print("running the train.py file")
            train_process=subprocess.Popen(['python', 'train.py'])
            train_process.wait()
            print("running the main.py file")
            main_process=subprocess.Popen(['python', 'main.py'])
            return 'File uploaded successfully!'
        return send_from_directory('Sailor', 'cricketFile.html')

@app.route('/Tabletennis.html')
def tennis():
    return send_from_directory('Sailor','Tabletennis.html')

# Define another route
@app.route('/about.html')
def about():
    return send_from_directory('Sailor','about.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)

