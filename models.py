class Jogo:
    # colcoar o none no id quer dizer que ele vai ou nao ter um id, vai ser parametro opcional
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha