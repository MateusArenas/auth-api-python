
from flask import Flask, request, jsonify

from app import app

@app.route('/test', methods=['GET'])
def test():
    try:
        return jsonify(default=200)
    except Exception as e:
        return jsonify(message="Error Test \n %s" % (e)), 400