from flask import request, Blueprint
from controller.tomatoController import predict_tomato

tomato_route = Blueprint('tomato_route', __name__)

@tomato_route.route('/predict/tomato', methods=['POST'])
def predict_tomato_route():
    return predict_tomato(request)