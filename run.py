from acepraf import app, create_tables

if __name__ == '__main__':
    create_tables()  # Cria as tabelas antes de iniciar o servidor
    app.run(debug=True)
