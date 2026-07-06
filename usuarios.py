from flask import Flask, request
import sqlite3
import hashlib
import os

DB_NAME = "usuarios.db"

app = Flask(__name__)

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def agregar_usuario(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute(
            'INSERT INTO usuarios (username, password_hash) VALUES (?, ?)',
            (username, hashed)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_usuario(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM usuarios WHERE username = ?', (username,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is None:
        return False
    return resultado[0] == hash_password(password)

@app.route('/')
def index():
    return '<h1>Sistema de Control de Credenciales</h1><p>Servidor Flask operativo en puerto 5800</p>'

@app.route('/registro')
def registro():
    usuario = request.args.get('usuario')
    clave = request.args.get('clave')

    if not usuario or not clave:
        return 'Debe indicar usuario y clave.'

    if agregar_usuario(usuario, clave):
        return f'Usuario {usuario} registrado correctamente con contraseña en hash.'
    else:
        return f'El usuario {usuario} ya existe.'

@app.route('/login')
def login():
    usuario = request.args.get('usuario')
    clave = request.args.get('clave')

    if not usuario or not clave:
        return 'Debe indicar usuario y clave.'

    if verificar_usuario(usuario, clave):
        return f'Acceso concedido. Bienvenido, {usuario}!'
    else:
        return 'Acceso denegado. Usuario o clave incorrectos.'

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5800)

