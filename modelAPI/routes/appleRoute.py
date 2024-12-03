from flask import request, Blueprint
from controller.appleController import predict_apple

apple_route = Blueprint('apple_route', __name__)

@apple_route.route('/predict/apple', methods=['POST'])
def predict_apple_route():
    return predict_apple(request)