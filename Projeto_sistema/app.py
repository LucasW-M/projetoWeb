
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo'  # Usado para sessão (login)

# Criar banco se não existir
def init_db():
    with sqlite3.connect('usuarios.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT UNIQUE NOT NULL,
                            senha TEXT NOT NULL)''')

# Página inicial (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
            if cursor.fetchone():
                session['usuario'] = usuario
                return redirect(url_for('dashboard'))
        return 'Usuário ou senha inválidos'
    return render_template('login.html')

# Página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        with sqlite3.connect('usuarios.db') as conn:
            try:
                conn.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return 'Usuário já existe'
    return render_template('cadastro.html')

# Área protegida
@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

