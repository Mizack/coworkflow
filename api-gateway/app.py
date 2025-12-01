from flask import Flask, request, jsonify
import requests
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

SERVICES = {
    'auth': 'http://ms-usuarios:5001',
    'users': 'http://ms-usuarios:5001',
    'spaces': 'http://ms-espacos:5002',
    'reservations': 'http://ms-reservas:5003',
    'payments': 'http://ms-pagamentos:5004',
    'pricing': 'http://ms-precos:5005',
    'checkin': 'http://ms-checkin:5006',
    'notify': 'http://ms-notificacoes:5007',
    'financial': 'http://ms-financeiro:5008',
    'analytics': 'http://ms-analytics:5009'
}

def verify_token():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None

@app.route('/<service>/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, endpoint):
    if service not in SERVICES:
        return jsonify({'error': 'Service not found'}), 404
    
    # Verificar autenticação para rotas protegidas
    protected_routes = ['users', 'reservations', 'payments', 'checkin', 'financial', 'analytics']
    if service in protected_routes and not verify_token():
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Proxy para o microsserviço
    url = f"{SERVICES[service]}/{endpoint}"
    
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k != 'Host'},
            data=request.get_data(),
            params=request.args,
            allow_redirects=False
        )
        return response.content, response.status_code, response.headers.items()
    except:
        return jsonify({'error': 'Service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)