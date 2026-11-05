from .configuracoes import DURACAO_QUADRO


class Animacao:
    def __init__(self, quadros, duracao_quadro=DURACAO_QUADRO):
        self._quadros = quadros
        self._duracao_quadro = duracao_quadro
        self._indice = 0
        self._tempo = 0

    @property
    def quadro_atual(self):
        return self._quadros[self._indice]

    def atualizar(self, dt):
        self._tempo += dt
        while self._tempo >= self._duracao_quadro:
            self._tempo -= self._duracao_quadro
            self._indice = (self._indice + 1) % len(self._quadros)

    def reiniciar(self):
        self._indice = 0
        self._tempo = 0

