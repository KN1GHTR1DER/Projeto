#usuários.py
from werkzeug.security import generate_password_hash
from banco import conectar_banco

# Conexão com o banco de dados
conexao = conectar_banco()
cursor = conexao.cursor()

# Inserir um paciente de teste
cursor.execute('''
INSERT INTO usuarios (nome, email, senha, tipo_usuario)
VALUES (?, ?, ?, ?)
''', ("Teste Paciente", "paciente@email.com", generate_password_hash("senha123"), "Paciente"))

# Inserir um profissional de saúde de teste
cursor.execute('''
INSERT INTO usuarios (nome, email, senha, tipo_usuario, especialidade, crm)
VALUES (?, ?, ?, ?, ?, ?)
''', ("Teste Profissional", "profissional@email.com", generate_password_hash("senha123"), "Profissional", "Cardiologia", "123456"))

# Confirmar e fechar conexão
conexao.commit()
conexao.close()

print("Usuários de teste inseridos com sucesso.")
