from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'secret-key'

API_BASE = 'http://api-gateway:8000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(f'{API_BASE}/auth/login', json=request.form.to_dict())
        if response.status_code == 200:
            session['token'] = response.json()['token']
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect('/login')
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    spaces = requests.get(f'{API_BASE}/spaces', headers=headers).json()
    analytics = requests.get(f'{API_BASE}/analytics/dashboard', headers=headers).json()
    
    return render_template('dashboard.html', spaces=spaces, analytics=analytics)

@app.route('/spaces')
def spaces():
    if 'token' not in session:
        return redirect('/login')
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    spaces = requests.get(f'{API_BASE}/spaces', headers=headers).json()
    
    return render_template('spaces.html', spaces=spaces)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)