from flask import request, Blueprint
from controller.grapeController import predict_grape

grape_route = Blueprint('grape_route', __name__)

@grape_route.route('/predict/grape', methods=['POST'])
def grape_apple_route():
    return predict_grape(request)