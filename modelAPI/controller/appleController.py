import logging
from flask import jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import numpy as np

model = load_model('models/apple_model_2.h5')

logging.basicConfig(level=logging.DEBUG)

class_labels = ['Apple__Apple_scab', 'Apple__Black_rot', 'Apple__Cedar_apple_rust', 'Apple__healthy', 'Not__apple']

disease_info = {
    'Apple__Apple_scab': {
        'name': 'Apple Scab',
        'description': 'Apple scab is a fungal disease that causes dark, sunken lesions on apples.',
        'treatment': [
            'Grow scab-resistant apple cultivars such as Akane, Chehalis, Liberty, Prima, and Tydeman Red.',
            'Apply nitrogen to fallen leaves in the fall to increase decomposition and make them more palatable to earthworms. Use liquid fish solution or 16-16-16 fertilizer.',
            'Shred fallen leaves in the fall with a lawn mower to speed up decomposition.',
            'Prune trees to improve air circulation.',
            'Avoid wetting foliage when watering.',
            'Apply dolomitic lime in the fall to increase pH and reduce fungal spores.',
            'Spray fungicides (Bonide Captan, wettable sulfur, summer lime sulfur, or Spectracide Immunox) when temperatures are above 60°F and leaves or flowers are wet.'
        ]
    },
    'Apple__Black_rot': {
        'name': 'Black Rot',
        'description': 'Black rot is caused by a fungal pathogen that affects apples, turning them black and rotting.',
        'treatment': [
            'Sanitize the garden by clearing fallen leaves, rotten fruit, and other plant debris.',
            'Prune infected plant parts and dispose of them away from the garden.',
            'Prune regularly to improve air circulation and reduce humidity.',
            'Use fungicides containing captan or chlorothalonil according to the recommended dosage and usage.'
        ]
    },
    'Apple__Cedar_apple_rust': {
        'name': 'Cedar Apple Rust',
        'description': 'Cedar apple rust is a fungal disease that causes yellow-orange spots on the leaves and fruit.',
        'treatment': [
            'Plant resistant cultivars such as Golden Supreme, Pioneer Mac, Sansa, Enterprise, and Gala Supreme.',
            'Plant apple and cedar trees at least one mile apart to reduce the spread of the disease.',
            'Remove and destroy galls from cedar trees before the telial horns form in the spring.',
            'Apply fungicides like Myclobutanil (Immunox), Bordeaux mixture, Captan, or Captan + Mancozeb from the time flower buds appear until the weather is warm and dry.',
            'Inspect nearby juniper and red cedar trees in late winter or early spring.',
            'Prune and remove brown, woody galls.'
        ]
    },
    'Apple__healthy': {
        'name': 'Healthy Apple',
        'description': 'The apple is free from any visible diseases or pests.',
        'treatment': ['No treatment needed. Continue regular care.']
    },
    'Not__apple': {
        'name': 'Not Apple',
        'description': 'The item is not an apple.',
        'treatment': ['N/A']
    }
}

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

        disease_data = disease_info.get(predicted_label, {
            'name': 'Unknown Disease',
            'description': 'No description available.',
            'treatment': 'No treatment information available.'
        })

        response = {
            'confidence': round(confidence * 100, 2),
            'label': predicted_label,
            'disease_info': {
                'name': disease_data['name'],
                'description': disease_data['description'],
                'treatment': disease_data['treatment']
            }
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return jsonify({'error': 'Invalid image file'}), 400