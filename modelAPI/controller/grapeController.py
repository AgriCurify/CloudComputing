import logging
from flask import jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import numpy as np

model = load_model('models/grape_model_2.h5')

logging.basicConfig(level=logging.DEBUG)

class_labels = [ 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'not_anggur' ]

disease_info = {
    'Grape___Black_rot': {
        'name': 'Grape Black Rot',
        'description': 'Grape black rot is a fungal disease that causes dark, sunken lesions on grape berries and can lead to premature fruit drop.',
        'treatment': [
            'Use copper-based or mancozeb fungicides regularly, especially during humid weather.',
            'Remove infected leaves or fruits to reduce the source of inoculum.',
            'Avoid planting grapes in previously infected areas for several years to reduce the chance of re-infection.',
            'Ensure that the plant canopy is open to increase air circulation and reduce humidity.'
        ]
    },
    'Grape___Esca_(Black_Measles)': {
        'name': 'Grape Esca (Black Measles)',
        'description': 'Grape Esca, also known as Black Measles, is a fungal disease that causes dark streaks and necrosis in grapevine wood, affecting both leaves and fruit.',
        'treatment': [
            'Remove infected plant parts immediately to limit the spread of the fungus.',
            'Use biocontrols like Trichoderma spp. to inhibit pathogen development.',
            'Ensure there are no wounds on the roots or rootstock to prevent pathogen entry.',
            'Apply systemic fungicides such as phosphite to suppress disease development.'
        ]
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        'name': 'Grape Leaf Blight (Isariopsis Leaf Spot)',
        'description': 'Grape leaf blight, caused by Isariopsis, leads to dark lesions with a yellow halo on grape leaves, and can cause premature leaf drop.',
        'treatment': [
            'Collect and destroy fallen or infected leaves to prevent disease spread.',
            'Use contact fungicides such as chlorothalonil or mancozeb during the growing season.',
            'Avoid overhead irrigation to minimize leaf moisture and reduce disease spread.',
            'Consider using grape varieties that are resistant to this disease.'
        ]
    },
    'Grape___healthy': {
        'name': 'Healthy Grape',
        'description': 'The grapevine is free from any visible diseases or pests.',
        'treatment': ['No treatment needed. Continue regular care and maintenance.']
    },
    'not_anggur': {
        'name': 'Not Grape',
        'description': 'The item is not a grapevine.',
        'treatment': ['N/A']
    }
}

def preprocess_image(img):
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_grape(request):
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