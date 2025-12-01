from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@db-espacos:5432/espacos'
db = SQLAlchemy(app)
swagger = Swagger(app)

class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    photo_url = db.Column(db.String(255))

@app.route('/spaces', methods=['GET'])
def get_spaces():
    """Lista espaços
    ---
    responses:
      200:
        description: Lista de espaços
    """
    spaces = Space.query.all()
    return jsonify([{
        'id': s.id, 'name': s.name, 'description': s.description,
        'capacity': s.capacity, 'price_per_hour': s.price_per_hour,
        'photo_url': s.photo_url
    } for s in spaces])

@app.route('/spaces', methods=['POST'])
def create_space():
    """Criar espaço
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            name:
              type: string
            description:
              type: string
            capacity:
              type: integer
            price_per_hour:
              type: number
    """
    data = request.json
    space = Space(**data)
    db.session.add(space)
    db.session.commit()
    return jsonify({'id': space.id}), 201

@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space(space_id):
    """Detalhes do espaço
    ---
    parameters:
      - name: space_id
        in: path
        type: integer
        required: true
    """
    space = Space.query.get_or_404(space_id)
    return jsonify({
        'id': space.id, 'name': space.name, 'description': space.description,
        'capacity': space.capacity, 'price_per_hour': space.price_per_hour,
        'photo_url': space.photo_url
    })

@app.route('/spaces/<int:space_id>/availability', methods=['GET'])
def check_availability(space_id):
    """Verificar disponibilidade
    ---
    parameters:
      - name: space_id
        in: path
        type: integer
        required: true
      - name: date
        in: query
        type: string
        required: true
    """
    return jsonify({'available': True, 'slots': ['09:00', '10:00', '14:00']})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)