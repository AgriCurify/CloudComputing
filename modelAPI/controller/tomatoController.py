import logging
from flask import jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import numpy as np

model = load_model('models/tomato_model_3.h5')

logging.basicConfig(level=logging.DEBUG)

class_labels = ['Not_Tomato', 'Tomato___Bacterial_spot', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

disease_info = {
    'Not_Tomato': {
        'name': 'Not Tomato',
        'description': 'The item is not a tomato.',
        'treatment': ['N/A']
    },
    'Tomato___Bacterial_spot': {
        'name': 'Tomato Bacterial Spot',
        'description': 'Bacterial spot causes dark, water-soaked lesions on leaves, stems, and fruit, leading to defoliation and fruit loss.',
        'treatment': [
            'Use certified disease-free seeds and plants.',
            'Avoid overhead watering and use drip or furrow irrigation.',
            'Remove and dispose of infected plant material.',
            'Prune plants to improve air circulation.',
            'Spray with copper-based fungicides for control.',
            'Practice crop rotation and avoid planting tomatoes in areas previously affected by bacterial spot.'
        ]
    },
    'Tomato___Leaf_Mold': {
        'name': 'Tomato Leaf Mold',
        'description': 'Leaf mold is a fungal disease that affects the leaves of tomato plants, causing yellowing and mold growth on the undersides of leaves.',
        'treatment': [
            'Improve air circulation by spacing plants apart, pruning lower leaves, and avoiding excess nitrogen fertilization.',
            'Avoid overhead watering and use drip irrigation.',
            'Remove infected leaves and debris.',
            'Apply fungicides such as chlorothalonil, mancozeb, and azoxystrobin as a preventive measure.',
            'Consider using biofungicides and copper sprays.',
            'Rotate crops and remove infected plants immediately.'
        ]
    },
    'Tomato___Septoria_leaf_spot': {
        'name': 'Tomato Septoria Leaf Spot',
        'description': 'Septoria leaf spot causes small, dark spots with light centers on the leaves, leading to defoliation and reduced yields.',
        'treatment': [
            'Use tomato-specific fungicides or biofungicides like Serenade.',
            'Remove and dispose of infected leaves to reduce spread.',
            'Practice good garden sanitation by cleaning equipment and removing plant debris.',
            'Rotate crops every three years to break the disease cycle.',
            'Apply copper sprays and other fungicides to control the spread.'
        ]
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        'name': 'Tomato Spider Mites (Two-Spotted Spider Mite)',
        'description': 'Spider mites cause yellowing, stippling, and webbing on tomato plants, weakening them and reducing yield.',
        'treatment': [
            'Pull out and destroy infected plants, do not compost.',
            'Spray plants with water to remove mites from leaves.',
            'Apply insecticidal soap, horticultural oil, or neem oil to infested plants.',
            'Use chili pepper solution or sulfur-based fungicides to reduce mite populations.',
            'Use miticides such as Dynamec, Oberon, or Omite for effective control.',
            'Control weeds, encourage natural predators like ladybirds and lacewings, and ensure adequate irrigation.'
        ]
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'name': 'Tomato Yellow Leaf Curl Virus',
        'description': 'Tomato yellow leaf curl virus is transmitted by whiteflies and causes yellowing, curling, and stunted growth in tomato plants.',
        'treatment': [
            'Uproot and destroy infected plants immediately to prevent further spread.',
            'Control whitefly populations using horticultural oils or reflective mulches.',
            'Keep the area free of weeds that can serve as hosts for whiteflies.',
            'Consider using low-concentration canola oil sprays to reduce whitefly feeding.',
            'Use virus-resistant tomato varieties and rotate crops to non-host plants.'
        ]
    },
    'Tomato___Tomato_mosaic_virus': {
        'name': 'Tomato Mosaic Virus',
        'description': 'Tomato mosaic virus causes mottled, distorted leaves and stunted growth. It is spread by aphids and infected tools.',
        'treatment': [
            'Remove infected plants and dispose of them away from the garden.',
            'Disinfect all tools, equipment, and work surfaces used in the garden.',
            'Use resistant tomato varieties such as those containing Tm-1, Tm-2, and Tm-2² resistance genes.',
            'Rotate crops to non-host varieties.',
            'Control aphids and thrips to reduce transmission.',
            'Maintain good garden hygiene and avoid planting downwind of infected areas.'
        ]
    },
    'Tomato___healthy': {
        'name': 'Healthy Tomato',
        'description': 'The tomato plant is free from any visible diseases or pests.',
        'treatment': ['No treatment needed. Continue regular care and maintenance.']
    }
}

def preprocess_image(img):
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_tomato(request):
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