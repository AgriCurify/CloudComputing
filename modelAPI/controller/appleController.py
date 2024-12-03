import logging
from flask import jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import numpy as np

model = load_model('models/apple_model_1.h5')

logging.basicConfig(level=logging.DEBUG)

class_labels = ['Apple__Apple_scab', 'Apple__Black_rot', 'Apple__Cedar_apple_rust', 'Apple__healthy', 'Not__apple']

def preprocess_image(img):
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_apple(request):
    if 'file' not in request.files:
        logging.error('No file found')
        return jsonify({'error': 'No file found'})
    
    file = request.files['file']

    if file.filename == '':
        logging.error('No filename provided')
        return jsonify({'error': 'No filename provided'})
    
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        logging.error('Invalid file type')
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, or JPEG files are allowed.'}), 400

    try:
        img = image.load_img(io.BytesIO(file.read()), target_size=(224, 224))
        x = image.img_to_array(img)
        x = preprocess_image(x) 

        predictions = model.predict(x)
        predicted_class_index = np.argmax(predictions)

        predicted_label = class_labels[predicted_class_index]
        confidence = float(np.max(predictions))

        response = {
            'confidence': round(confidence * 100, 2),
            'prediction': predicted_label
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return jsonify({'error': 'Invalid image file'}), 400