import random
from abc import abstractmethod

from .combatente import Combatente
from .configuracoes import VELOCIDADE_INIMIGO


class InimigoBot(Combatente):
    DIRECOES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    INTERVALO_DECISAO = 1.0

    def __init__(self, nome, x, y, caminho_sprite):
        super().__init__(nome, x, y, VELOCIDADE_INIMIGO, caminho_sprite)
        self._direcao_x = 0
        self._direcao_y = 0
        self._tempo_desde_decisao = self.INTERVALO_DECISAO

    @abstractmethod
    def tomar_decisao(self):
        pass

    def escolher_direcao_aleatoria(self):
        self._direcao_x, self._direcao_y = random.choice(self.DIRECOES)
        self._tempo_desde_decisao = 0

    def atualizar(self, dt, fase):
        self._tempo_desde_decisao += dt
        if self._tempo_desde_decisao >= self.INTERVALO_DECISAO:
            self.tomar_decisao()

        moveu = self.mover(self._direcao_x, self._direcao_y, dt, fase)
        if not moveu:
            self.tomar_decisao()

        self._atualizar_animacao(dt)
