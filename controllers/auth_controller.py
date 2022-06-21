from flask import Flask, request, jsonify
import json
import bcrypt
import jwt
import os

from app import app

from modules.email import transporter

from schemas.User import User

from middlewares.auth import auth_verify

from utils.json import useJSON

authConfig = useJSON('../config/auth.json')

from datetime import datetime, timedelta

from pytz import timezone

tz = timezone('America/Sao_Paulo')

def generate_refresh_token (params = {}):
    return jwt.encode(
        payload={ 
            'exp':  datetime.now().astimezone(tz) + timedelta(days=1),
            'aud': "RefreshToken.API",
            'iss': 'http://localhost',
            **params 
        },
        key=authConfig['secret']
    )

def generate_token (params): 
    return jwt.encode(
        payload={ 
            'exp':  datetime.now().astimezone(tz) + timedelta(hours=2),
            **params 
        },
        key=authConfig['secret']
    )


def to_json(document):
    data = json.loads(document.to_json())
    data['_id'] = data['_id']['$oid']
    return data

#this search not trow exception in request, is isolated.
def findOne(schema, query):
    try:
        document = schema.objects.get(**query)
        return document
    except Exception as e:
        return None

@app.route("/user-recover", methods=['GET'])
def user_recover():
    try:
        auth = auth_verify(request.headers['authorization'])

        if auth == None:
            raise Exception('This user is not auth.')

        user = findOne(User, { 'id': auth })

        if user == None: 
            raise Exception('Invalid User for Auth Token.')

        return jsonify(user=to_json(user))
    except Exception as e:
        return jsonify(message="Recover failed \n %s" % (e)), 400


@app.route("/refresh-token", methods=['POST'])
def refresh_token ():
    try:
        body = request.get_json()

        decoded = jwt.verify(body['token'], authConfig.secret, {
            'aud': "RefreshToken.API",
            'iss': 'http://localhost',
        })

        header_data = jwt.get_unverified_header(body['token'])

        decoded = jwt.decode(body['token'], 
            key=authConfig['secret'], 
            algorithms=[header_data['alg']],
            issuer="http://localhost",
            audience="RefreshToken.API",
        )

        return jsonify(
            token=generate_token({ 'sub': str(decoded['sub']) }),
            refreshtoken=generate_refresh_token({ 'sub': str(decoded['sub']) })
        )
    except Exception as e:
        return jsonify(message="Error Refresh Token \n %s" % (e)), 400

@app.route("/login", methods=['POST'])
def login():
    try:
        body = request.get_json()

        user = findOne(User, { 'email': body['email'] })

        if user == None:
            raise Exception('Invalid email or phone filed User not found')
        
        if bcrypt.checkpw(body['password'], user['password']):
            print('password ok')
        else:
            raise Exception('Invalid Password')


        return jsonify(
            user=to_json(user),
            token=generate_token({ 'sub': str(user.id) }),
            refreshtoken=generate_refresh_token({ 'sub': str(user.id) })
        )
    
    except Exception as e:
        return jsonify(message="Error Login \n %s" % (e)), 400


@app.route("/register", methods=['POST'])
def register():
    try:
        verifiedToken = os.urandom(20).hex()

        body = request.get_json()

        user = User(email=body['email'], password=body['password'], verifiedToken=verifiedToken).save()

        transporter.send_mail({ 
            'to': user.email, 
            'subject': 'Enviando',
            'from': 'simplechatpop@gmail.com', 
            'template': 'home/welcome'
        })

        transporter.send_mail({
            'to': user.email,
            'from': 'simplechatpop@gmail.com',
            'subject': 'Enviando',
            'template': 'auth/verify',
            'context': { 'url': 'http://localhost/verify/{token}'.format(token=verifiedToken) },
        })

        return jsonify(
            user=to_json(user),
            token=generate_token({ 'sub': str(user.id) }),
            refreshtoken=generate_refresh_token({ 'sub': str(user.id) })
        )
    except Exception as e:
        return jsonify(message="Error Register \n %s" % (e)), 400


@app.route('/verify/<token>', methods=['GET'])
def verify (token):
    try:
        if token == None: 
            raise Exception('No token provider')

        user = findOne(User, { 'verifiedToken': token })

        if user == None: 
            raise Exception("User invalid or link")

        user.update(unset__verifiedToken=True, unset__expiredAt=True, verified=True)

        return jsonify(
            message="email verified sucessfully"
        )
    except Exception as e:
        return jsonify(message="Error Verify Token \n %s" % (e)), 400

@app.route('/verify-acess', methods=['GET'])
def verify_acess():
    try:
        auth = auth_verify(request.headers['authorization'])

        user = findOne(User, { 'id': auth, verified: True })

        if user == None:
            raise Exception("User is not verified")

        return jsonify(
            user=to_json(user),
        )
    except Exception as e:
        return jsonify(message="Error Verify Acess \n %s" % (e)), 400
