from flask import Flask, render_template, request, session, redirect, url_for,jsonify,json
from dotenv import load_dotenv
import os
from db import conectar_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto_para_pruebas')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simulación simple de login (acepta cualquier usuario)
        username = request.form.get('username')
        session['user'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        contraseña = request.form.get('contraseña')
        correo = request.form.get('correo')
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        # 1. BUSCAR SI EL CORREO YA EXISTE
        cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s", (correo,))
        usuario_existente = cursor.fetchone()
        
        if usuario_existente:
            # Si el correo ya está en la DB, cerramos la conexión y avisamos
            conn.close()
            return "El correo ya está registrado. Intenta con otro o inicia sesión.", 400
        
        # 2. SI NO EXISTE, PROCEDEMOS A INSERTAR
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, contraseña, correo) VALUES (%s, %s, %s)", 
                (username, contraseña, correo)
            )
            conn.commit()
        except Exception as e:
            print(f"Error al insertar: {e}")
            return "Hubo un error en el registro", 500
        finally:
            conn.close()
            
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/validar_correo', methods=['POST'])
def validar_correo():
    data = request.get_json()
    correo = data.get('correo')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM usuarios WHERE correo = %s", (correo,))
    existe = cursor.fetchone() is not None
    conn.close()
    
    return jsonify(disponible=not existe)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)