import io
import os
import subprocess

from flask import Flask, jsonify, request
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    pdf_file = request.files['file']
    
    # Check that the uploaded file is a PDF file
    if pdf_file.content_type != 'application/pdf':
        return jsonify({'error': 'Invalid file type'})
    
    # Convert the PDF to an image using pdftoppm
    pdf_buffer = pdf_file.read()
    process = subprocess.Popen(['pdftoppm', '-png', '-singlefile', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate(input=pdf_buffer)
    if process.returncode != 0:
        return jsonify({'error': 'Failed to convert PDF to image'})
    
    # Open the image with PIL
    image = Image.open(io.BytesIO(stdout))
    
    # Run OCR on the image using Tesseract
    text = pytesseract.image_to_string(image)
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
