import sqlite3

# Conecte-se ao banco de dados
conn = sqlite3.connect('terrenos.db')
cursor = conn.cursor()

# Adicione a coluna imagem se ela não existir
try:
    cursor.execute("ALTER TABLE diretoria ADD COLUMN imagem BLOB")
    print("Coluna 'imagem' adicionada com sucesso!")
except sqlite3.OperationalError as e:
    print(f"Erro: {e}")

# Confirme as alterações e feche a conexão
conn.commit()
conn.close()
