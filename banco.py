#banco.py
import sqlite3

# Função para inicializar o banco de dados (criação de tabelas)
def inicializar_banco():
    conexao = sqlite3.connect('clinica.db')
    cursor = conexao.cursor()

    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL,
        especialidade TEXT,
        crm TEXT,
        telefone TEXT
    )
    ''')

    # Tabela de consultas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER NOT NULL,
        id_profissional INTEGER NOT NULL,
        data_hora TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Agendada',
        observacoes TEXT,
        FOREIGN KEY (id_paciente) REFERENCES usuarios (id),
        FOREIGN KEY (id_profissional) REFERENCES usuarios (id)
    )
    ''')

    # Tabela de prontuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prontuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER NOT NULL,
        id_profissional INTEGER NOT NULL,
        data TEXT NOT NULL,
        anotacoes_medicas TEXT NOT NULL,
        prescricoes TEXT,
        FOREIGN KEY (id_paciente) REFERENCES usuarios (id),
        FOREIGN KEY (id_profissional) REFERENCES usuarios (id)
    )
    ''')

    conexao.commit()
    conexao.close()

# Função para conectar ao banco de dados
def conectar_banco():
    return sqlite3.connect('clinica.db')
