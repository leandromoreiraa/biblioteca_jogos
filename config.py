import os
#confi da aplicacao

SECRET_KEY = "games"

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD= "admin"
MYSQL_DB = "jogoteca"
MYSQL_PORT = 3306
#para salvar os arquivos em um caminhoo absoluto, e consigo acessar esse caminho em qualqer lugar da minha aplicacao
UPLOAD_PATH= os.path.dirname(os.path.abspath(__file__)) + '/uploads'