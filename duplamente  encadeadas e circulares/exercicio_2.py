class Musica:
    def __init__(self, codigo, titulo, artista,
    duracao):
        self.codigo = codigo
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao
        self.anterior = None
        self.proximo = None