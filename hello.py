from flask import Flask # type: ignore
import json
from .users import user

app = Flask(__name__)

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


if __name__ == "__main__":
    
    app.run(debug=True)