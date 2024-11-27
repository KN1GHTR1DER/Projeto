from flask import Flask, render_template, request, redirect, url_for, session
from banco import inicializar_banco, conectar_banco
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializa o banco de dados
inicializar_banco()

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Função para autenticar o usuário
def autenticar_usuario(email, senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario and check_password_hash(usuario[3], senha):  # Verifica a senha
        return {'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'tipo_usuario': usuario[4]}
    return None

# Rota inicial redireciona para login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = autenticar_usuario(email, senha)
        
        if usuario:
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['tipo_usuario'] = usuario['tipo_usuario']
            
            if usuario['tipo_usuario'] == 'Paciente':
                return redirect(url_for('paciente_dashboard'))
            else:
                return redirect(url_for('profissional_dashboard'))
        else:
            return render_template('login.html', mensagem='Credenciais inválidas')
    
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard do paciente
@app.route('/paciente_dashboard')
def paciente_dashboard():
    if 'usuario_id' in session and session['tipo_usuario'] == 'Paciente':
        return render_template('paciente_dashboard.html', usuario_nome=session['usuario_nome'])
    else:
        return redirect(url_for('login'))

# Dashboard do profissional
@app.route('/profissional_dashboard')
def profissional_dashboard():
    if 'usuario_id' in session and session['tipo_usuario'] == 'Profissional':
        return render_template('profissional_dashboard.html', usuario_nome=session['usuario_nome'])
    else:
        return redirect(url_for('login'))

# Agendamento de consulta
@app.route('/agendar_consulta', methods=['GET', 'POST'])
def agendar_consulta():
    if 'usuario_id' in session and session['tipo_usuario'] == 'Paciente':
        if request.method == 'POST':
            profissional_id = request.form['profissional_id']
            data_hora = request.form['data_hora']
            
            # Inserir consulta no banco de dados
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute('''
            INSERT INTO consultas (id_paciente, id_profissional, data_hora, status)
            VALUES (?, ?, ?, 'Agendada')
            ''', (session['usuario_id'], profissional_id, data_hora))
            conexao.commit()
            conexao.close()
            return redirect(url_for('paciente_dashboard'))
        
        # Obter lista de profissionais
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, especialidade FROM usuarios WHERE tipo_usuario = "Profissional"')
        profissionais = cursor.fetchall()
        conexao.close()

        return render_template('agendar_consulta.html', profissionais=profissionais)
    else:
        return redirect(url_for('login'))

# Outros templates de exibição

if __name__ == '__main__':
    app.run(debug=True)

from banco import inicializar_banco
inicializar_banco()
print("Banco de dados inicializado.")
