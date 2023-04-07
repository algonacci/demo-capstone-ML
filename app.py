import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import module as md

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def root():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API!"
        }
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        image = request.files["image"]
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            result = md.face_mesh_predict(image_path)
            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success detect the face landmark",
                    # "data": "http://127.0.0.1:5000/" + result
                    "data": "http://192.168.0.107:5000/" + result
                }
            }), 200
        else:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "Please upload an image!"
                }
            }), 400
    else:
        return jsonify({
            "status": {
                "code": 403,
                "message": "USE POST!"
            }
        }), 403


@app.errorhandler(400)
def bad_request(error):
    return {
        "status": {
            "code": 400,
            "message": "Client side error!"
        }
    }, 400


@app.errorhandler(404)
def not_found(error):
    return {
        "status": {
            "code": 404,
            "message": "URL Not Found!"
        }
    }, 404


@app.errorhandler(405)
def method_not_allowed(error):
    return {
        "status": {
            "code": 405,
            "message": "Request method not allowed!"
        }
    }, 405


@app.errorhandler(500)
def internal_server_error(error):
    return {
        "status": {
            "code": 500,
            "message": "Server error!"
        }
    }, 500


if __name__ == "__main__":
    app.run()
