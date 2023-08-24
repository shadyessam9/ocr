from flask import Flask, request, jsonify, render_template
from PIL import Image
from pix2tex import cli as pix2tex 
import io

# Initialize the Flask application
app = Flask(__name__)

# Initialize the model
model = pix2tex.LatexOCR()

# Function to upload multiple files
def upload_files():
    uploaded_files = request.files.getlist("file")
    imgs = []
    for file in uploaded_files:
        if file.filename != '':
            imgs.append((file.filename, file))
    return imgs

# Route for uploading files
@app.route('/upload', methods=['POST'])
def upload_route():
    try:
        imgs = upload_files()
        predictions = []
        for name, f in imgs:
            # Add basic file type check (e.g., '.png', '.jpg')
            if name.split('.')[-1] in ['png', 'jpg', 'jpeg']:
                img = Image.open(io.BytesIO(f.read()))
                math = model(img)
                # Directly append the LaTeX math expression
                predictions.append(math)
            else:
                return jsonify({"error": "Invalid file type"}), 400

        result = '\\\\'.join(predictions)
        return render_template('index.html', result=result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# A default route for hello world
@app.route('/')
def hello_world():
    return render_template('index.html', result="")

if __name__ == '__main__':
    app.run(debug=True)
