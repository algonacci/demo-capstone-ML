from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def root():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API!"
        }
    }), 200


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
