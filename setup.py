from flask import Flask, request, jsonify
from PIL import Image
import io
from flask_cors import CORS
from pix2tex import cli as pix2tex  # Import based on your actual package

app = Flask(__name__)
CORS(app)

# Initialize the model
model = pix2tex.LatexOCR()  # Replace this with the actual initialization for your model

def hello():
    return 'hello'

# Function to upload multiple files
def upload_files():
    uploaded_files = request.files.getlist("file")
    imgs = []
    for file in uploaded_files:
        if file.filename != '':
            imgs.append((file.filename, file))
    return imgs

@app.route('/upload', methods=['POST'])
def upload_route():
    try:
        imgs = upload_files()
        predictions = []
        for name, f in imgs:
            if name.split('.')[-1] in ['png', 'jpg', 'jpeg']:
                img = Image.open(io.BytesIO(f.read()))
                math = model(img)  # Use your model to extract text here
                predictions.append(math)
            else:
                return jsonify({"error": "Invalid file type"}), 400

        return jsonify({"results": predictions}), 200  # Explicitly set status code to 200 OK
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def root_route():
    return hello()

if __name__ == '__main__':
    app.run(debug=True)
