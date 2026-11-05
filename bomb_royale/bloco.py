import pygame

from .configuracoes import COR_BLOCO, TAMANHO_CELULA
from .entidade import Entidade


class Bloco(Entidade):
    def __init__(self, x, y, destrutivel=False):
        super().__init__(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        self._destrutivel = destrutivel

    @property
    def destrutivel(self):
        return self._destrutivel

    def destruir(self):
        if self._destrutivel:
            self.desativar()

    def atualizar(self, dt, fase):
        pass

    def desenhar(self, tela):
        pygame.draw.rect(tela, COR_BLOCO, self.retangulo)

