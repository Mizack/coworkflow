from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@db-usuarios:5432/usuarios'
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)
swagger = Swagger(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(300))
    name = db.Column(db.String(100), nullable=False)

@app.route('/auth/signup', methods=['POST'])
def signup():
    """Cadastro de usuário
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            email:
              type: string
            password:
              type: string
            name:
              type: string
    """
    data = request.json
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        name=data['name']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    """Login de usuário
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            email:
              type: string
            password:
              type: string
    """
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/users/me', methods=['GET'])
def get_user():
    """Dados do usuário logado
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
    """
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        return jsonify({'id': user.id, 'email': user.email, 'name': user.name})
    except:
        return jsonify({'error': 'Invalid token'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)