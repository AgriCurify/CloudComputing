from flask import Flask
from routes.appleRoute import apple_route

app = Flask(__name__)

app.register_blueprint(apple_route)

if __name__ == '__main__':
    app.run(debug=True)