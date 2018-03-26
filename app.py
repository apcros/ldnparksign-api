from flask import Flask
import controllers.Api

app = Flask(__name__)

api = controllers.Api()


@app.route('/api/auth', methods=['GET'])
def load_login():
    api.login()


@app.route('/api/streets/signs', method=['GET'])
def list_available_signs():
    api.list_available_signs()


@app.route('/api/sign-request', method=['POST'])
def queue_sign_request():
    api.queue_sign_request()


@app.route('/api/street/<int:street_guid>/sign', method=['GET'])
def get_sign_for_street(street_guid):
    api.get_sign_for_street(street_guid)

