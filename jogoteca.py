from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
#aplicacao
app.config.from_pyfile('config.py')

#passar para dentro do banco / config do banco
db = MySQL(app)
#importar todas as views
from views import *

if __name__ == '__main__':
    # executa a aplicacao web com flask
    app.run(debug=True)


