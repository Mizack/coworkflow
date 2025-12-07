from flask import Flask, request, jsonify
import requests
import jwt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

USE_DOCKER = os.getenv('USE_DOCKER', 'false').lower() == 'true'

if USE_DOCKER:
    SERVICES = {
        'ms-usuarios': 'http://ms-usuarios:5001',
        'ms-espacos': 'http://ms-espacos:5002',
        'ms-reservas': 'http://ms-reservas:5003',
        'ms-pagamentos': 'http://ms-pagamentos:5004',
        'ms-precos': 'http://ms-precos:5005',
        'ms-checkin': 'http://ms-checkin:5006',
        'ms-notificacoes': 'http://ms-notificacoes:5007',
        'ms-financeiro': 'http://ms-financeiro:5008',
        'ms-analytics': 'http://ms-analytics:5009'
    }
else:
    SERVICES = {
        'ms-usuarios': 'http://localhost:5001',
        'ms-espacos': 'http://localhost:5002',
        'ms-reservas': 'http://localhost:5003',
        'ms-pagamentos': 'http://localhost:5004',
        'ms-precos': 'http://localhost:5005',
        'ms-checkin': 'http://localhost:5006',
        'ms-notificacoes': 'http://localhost:5007',
        'ms-financeiro': 'http://localhost:5008',
        'ms-analytics': 'http://localhost:5009'
    }

def verify_token():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None

@app.route('/auth/<path:endpoint>', methods=['GET', 'POST'])
def auth_proxy(endpoint):
    url = f"{SERVICES['ms-usuarios']}/auth/{endpoint}"
    print(url)
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={'Content-Type': 'application/json'},
            json=request.get_json() if request.is_json else None,
            params=request.args
        )
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/users/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users_proxy(endpoint):
    if not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    url = f"{SERVICES['ms-usuarios']}/users/{endpoint}"
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            json=request.get_json() if request.is_json else None,
            params=request.args
        )
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/spaces', methods=['GET', 'POST'])
@app.route('/spaces/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def spaces_proxy(endpoint=''):
    url = f"{SERVICES['ms-espacos']}/spaces" + (f"/{endpoint}" if endpoint else "")
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={'Content-Type': 'application/json'},
            json=request.get_json() if request.is_json else None,
            params=request.args
        )
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/reservations', methods=['GET', 'POST'])
@app.route('/reservations/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def reservations_proxy(endpoint=''):
    if not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    url = f"{SERVICES['ms-reservas']}/reservations" + (f"/{endpoint}" if endpoint else "")
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            json=request.get_json() if request.is_json else None,
            params=request.args
        )
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/payments/<path:endpoint>', methods=['POST'])
def payments_proxy(endpoint):
    if not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    url = f"{SERVICES['ms-pagamentos']}/payments/{endpoint}"
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={'Content-Type': 'application/json'},
            json=request.get_json()
        )
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/pricing/<path:endpoint>', methods=['POST'])
def pricing_proxy(endpoint):
    url = f"{SERVICES['ms-precos']}/pricing/{endpoint}"
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={'Content-Type': 'application/json'},
            json=request.get_json()
        )
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/checkin/<int:reservation_id>', methods=['POST'])
@app.route('/checkout/<int:reservation_id>', methods=['POST'])
def checkin_proxy(reservation_id):
    if not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    endpoint = 'checkin' if 'checkin' in request.path else 'checkout'
    url = f"{SERVICES['ms-checkin']}/{endpoint}/{reservation_id}"
    try:
        response = requests.post(url)
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/analytics/<path:endpoint>', methods=['GET'])
def analytics_proxy(endpoint):
    if not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    url = f"{SERVICES['ms-analytics']}/analytics/{endpoint}"
    try:
        response = requests.get(url)
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/financial/<path:endpoint>', methods=['GET'])
def financial_proxy(endpoint):
    if not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    url = f"{SERVICES['ms-financeiro']}/financial/{endpoint}"
    try:
        response = requests.get(url)
        return response.json(), response.status_code
    except:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)