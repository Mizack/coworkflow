from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@db-reservas:5432/reservas'
db = SQLAlchemy(app)
swagger = Swagger(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    space_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')
    total_price = db.Column(db.Float, nullable=False)

@app.route('/reservations', methods=['POST'])
def create_reservation():
    """Criar reserva
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            user_id:
              type: integer
            space_id:
              type: integer
            start_time:
              type: string
            end_time:
              type: string
            total_price:
              type: number
    """
    data = request.json
    reservation = Reservation(
        user_id=data['user_id'],
        space_id=data['space_id'],
        start_time=datetime.datetime.fromisoformat(data['start_time']),
        end_time=datetime.datetime.fromisoformat(data['end_time']),
        total_price=data['total_price']
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'id': reservation.id}), 201

@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    """Detalhes da reserva
    ---
    parameters:
      - name: reservation_id
        in: path
        type: integer
        required: true
    """
    reservation = Reservation.query.get_or_404(reservation_id)
    return jsonify({
        'id': reservation.id,
        'user_id': reservation.user_id,
        'space_id': reservation.space_id,
        'start_time': reservation.start_time.isoformat(),
        'end_time': reservation.end_time.isoformat(),
        'status': reservation.status,
        'total_price': reservation.total_price
    })

@app.route('/reservations/user/<int:user_id>', methods=['GET'])
def get_user_reservations(user_id):
    """Reservas do usuário
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    """
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': r.id, 'space_id': r.space_id,
        'start_time': r.start_time.isoformat(),
        'end_time': r.end_time.isoformat(),
        'status': r.status, 'total_price': r.total_price
    } for r in reservations])

@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    """Cancelar reserva
    ---
    parameters:
      - name: reservation_id
        in: path
        type: integer
        required: true
    """
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Reservation cancelled'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003)