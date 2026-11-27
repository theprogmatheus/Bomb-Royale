import pygame

from .configuracoes import (
    COR_BLOCO,
    COR_BLOCO_DESTRUTIVEL,
    COR_BLOCO_DESTRUTIVEL_BORDA,
    COR_BLOCO_DESTRUTIVEL_DESTAQUE,
    TAMANHO_CELULA,
)
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

    def receber_dano(self, quantidade):
        if quantidade > 0:
            self.destruir()

    def atualizar(self, dt, fase):
        pass

    def desenhar(self, tela):
        rect = self.retangulo
        if not self._destrutivel:
            pygame.draw.rect(tela, COR_BLOCO, rect)
            return

        # Caixote/tijolo rústico destrutível (16-bit)
        pygame.draw.rect(tela, COR_BLOCO_DESTRUTIVEL, rect)
        pygame.draw.line(tela, COR_BLOCO_DESTRUTIVEL_DESTAQUE, rect.topleft, (rect.right - 2, rect.top), 3)
        pygame.draw.line(tela, COR_BLOCO_DESTRUTIVEL_DESTAQUE, rect.topleft, (rect.left, rect.bottom - 2), 3)
        pygame.draw.line(tela, COR_BLOCO_DESTRUTIVEL_BORDA, (rect.left, rect.bottom - 2), (rect.right - 1, rect.bottom - 2), 3)
        pygame.draw.line(tela, COR_BLOCO_DESTRUTIVEL_BORDA, (rect.right - 2, rect.top), (rect.right - 2, rect.bottom - 1), 3)
        pygame.draw.rect(tela, (42, 26, 16), rect, 2)
        interno = rect.inflate(-14, -14)
        pygame.draw.rect(tela, COR_BLOCO_DESTRUTIVEL_BORDA, interno, 2)
        pygame.draw.line(tela, COR_BLOCO_DESTRUTIVEL_BORDA, interno.topleft, interno.bottomright, 2)
