from flask import Flask, logging # type: ignore
import json
from flask_cors import CORS, cross_origin
from .users import user

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:4200'], methods=['GET', 'POST', 'OPTIONS'])  # Allow specific origin and methods


    app.register_blueprint(user, url_prefix="/user")

    @app.route("/")
    def hello_world():
        data = {
            "name": "John Doe",
            "age": 30,
            "city": "New York"
            }
        json_data = json.dumps(data)    
        return json_data, 200, {"Content-Type": "application/json"}


    @app.route('/hello')
    def hello():
        return 'Everything is OK'
    return app   