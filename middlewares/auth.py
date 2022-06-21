from flask import jsonify, request
import jwt
import re

from utils.json import useJSON

authConfig = useJSON('../config/auth.json')

def auth_verify(authorization):
    try:
        if authorization == None:
            raise Exception('No token provider')

        parts = authorization.split(' ')

        if len(parts) is not 2:
            raise Exception('Token error')

        scheme, token = parts

        if re.search('Bearer', scheme) is None:
            raise Exception('Token malformatted')
        
        header_data = jwt.get_unverified_header(token)

        decode = jwt.decode(token, key=authConfig['secret'], algorithms=[header_data['alg'], ])

        return decode['sub']

    except Exception as e:
        return None