from flask import Flask, jsonify, request, session, make_response, render_template
from functools import wraps
import datetime
import jwt
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'topsecret'

def check_for_token(func):
    @wraps(func) 
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Il manque le token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token non valide'}),403
        return func(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Déjà connecté'

@app.route('/public')
def public():
    return 'Tout le monde peut le voir'

@app.route('/auth')
@check_for_token
def authorised():
    return 'Ceci est visible uniquement avec un token'

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
            },
            app.config['SECRET_KEY'])
        return token
        return jsonify({'token': jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])})
    else:
        return make_response('Mauvais mot de passe', 403, {'WWW-Authenticate': 'Basic realm: "Login Required"'})


@app.route('/logout', methods=['POST'])
def logout():
    return 'Déconnexion'

if __name__ == '__main__':  
    app.run(debug=True)
  
