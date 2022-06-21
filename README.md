# authenticate api in python

this api usage basic for authenticate, jtw, refresh token and email verification.


## Initialize
pip install virtualenv

venv\Scripts\activate 

pip install -r requirements.txt

## Update dependences > after initialize
(virtualenv) $ pip freeze > requirements.txt

## BEFORE Run API (Configure .env)
create .env file
your .env file...
export FLASK_APP="app"
export EMAIL_USER="myemail@gmail.com"
export EMAIL_PASS="mypassword123"

## Run API
flask run
