from flask import Flask, request, jsonify

app = Flask(__name__)

from mongoengine import *

connect(host='mongodb://localhost:27017/auth-db-py?retryWrites=true&w=majority')

from controllers.auth_controller import *
from controllers.test_controller import *
