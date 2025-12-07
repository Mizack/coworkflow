from flask import Flask, render_template, request, redirect, session, flash, jsonify
import requests
import datetime
import os

app = Flask(__name__)
app.secret_key = 'secret-key'

USE_DOCKER = os.getenv('USE_DOCKER', 'false').lower() == 'true'
API_BASE = 'http://api-gateway:8000' if USE_DOCKER else 'http://localhost:8000'

def get_headers():
    return {'Authorization': f'Bearer {session.get("token")}'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = requests.post(f'{API_BASE}/auth/signup', json=request.form.to_dict())
        if response.status_code == 201:
            flash('Usuário criado com sucesso!')
            return redirect('/login')
        flash('Erro ao criar usuário')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(f'{API_BASE}/auth/login', json=request.form.to_dict())
        if response.status_code == 200:
            session['token'] = response.json()['token']
            return redirect('/dashboard')
        flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect('/login')
    
    try:
        analytics = requests.get(f'{API_BASE}/analytics/dashboard', headers=get_headers()).json()
        return render_template('dashboard.html', analytics=analytics)
    except:
        flash('Erro ao carregar dashboard')
        return redirect('/login')

@app.route('/spaces')
def spaces():
    if 'token' not in session:
        return redirect('/login')
    
    spaces = requests.get(f'{API_BASE}/spaces').json()
    return render_template('spaces.html', spaces=spaces)

@app.route('/spaces/create', methods=['GET', 'POST'])
def create_space():
    if 'token' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'capacity': int(request.form['capacity']),
            'price_per_hour': float(request.form['price_per_hour'])
        }
        response = requests.post(f'{API_BASE}/spaces', json=data, headers=get_headers())
        if response.status_code == 201:
            flash('Espaço criado com sucesso!')
            return redirect('/spaces')
        flash('Erro ao criar espaço')
    return render_template('create_space.html')

@app.route('/reservations')
def reservations():
    if 'token' not in session:
        return redirect('/login')
    
    user = requests.get(f'{API_BASE}/users/me', headers=get_headers()).json()
    reservations = requests.get(f'{API_BASE}/reservations/user/{user["id"]}', headers=get_headers()).json()
    return render_template('reservations.html', reservations=reservations)

@app.route('/reserve/<int:space_id>', methods=['GET', 'POST'])
def reserve_space(space_id):
    if 'token' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        user = requests.get(f'{API_BASE}/users/me', headers=get_headers()).json()
        
        # Calcular preço
        pricing_data = {
            'space_id': space_id,
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'user_plan': 'basic'
        }
        price_response = requests.post(f'{API_BASE}/pricing/calc', json=pricing_data)
        total_price = price_response.json()['total']
        
        # Criar reserva
        reservation_data = {
            'user_id': user['id'],
            'space_id': space_id,
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'total_price': total_price
        }
        response = requests.post(f'{API_BASE}/reservations', json=reservation_data, headers=get_headers())
        
        if response.status_code == 201:
            reservation_id = response.json()['id']
            
            # Processar pagamento
            payment_data = {
                'reservation_id': reservation_id,
                'amount': total_price,
                'method': request.form['payment_method']
            }
            requests.post(f'{API_BASE}/payments/charge', json=payment_data, headers=get_headers())
            
            flash('Reserva criada e pagamento processado!')
            return redirect('/reservations')
        flash('Erro ao criar reserva')
    
    space = requests.get(f'{API_BASE}/spaces/{space_id}').json()
    return render_template('reserve.html', space=space)

@app.route('/checkin/<int:reservation_id>')
def checkin(reservation_id):
    if 'token' not in session:
        return redirect('/login')
    
    response = requests.post(f'{API_BASE}/checkin/{reservation_id}', headers=get_headers())
    if response.status_code == 200:
        flash('Check-in realizado com sucesso!')
    else:
        flash('Erro no check-in')
    return redirect('/reservations')

@app.route('/checkout/<int:reservation_id>')
def checkout(reservation_id):
    if 'token' not in session:
        return redirect('/login')
    
    response = requests.post(f'{API_BASE}/checkout/{reservation_id}', headers=get_headers())
    if response.status_code == 200:
        flash('Check-out realizado com sucesso!')
    else:
        flash('Erro no check-out')
    return redirect('/reservations')

@app.route('/cancel/<int:reservation_id>')
def cancel_reservation(reservation_id):
    if 'token' not in session:
        return redirect('/login')
    
    response = requests.delete(f'{API_BASE}/reservations/{reservation_id}', headers=get_headers())
    if response.status_code == 200:
        flash('Reserva cancelada com sucesso!')
    else:
        flash('Erro ao cancelar reserva')
    return redirect('/reservations')

@app.route('/financial')
def financial():
    if 'token' not in session:
        return redirect('/login')
    
    revenue = requests.get(f'{API_BASE}/financial/revenue', headers=get_headers()).json()
    expenses = requests.get(f'{API_BASE}/financial/expenses', headers=get_headers()).json()
    return render_template('financial.html', revenue=revenue, expenses=expenses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)