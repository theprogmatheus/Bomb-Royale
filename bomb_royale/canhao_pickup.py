import pygame

from .colisor import Colisor
from .combatente import Combatente
from .configuracoes import TAMANHO_CELULA
from .entidade import Entidade
from .arma_canhao import ArmaCanhao


class CanhaoPickup(Entidade):
    TAMANHO = TAMANHO_CELULA // 2
    COR = (220, 60, 60)

    def __init__(self, x, y):
        super().__init__(x, y, self.TAMANHO, self.TAMANHO)

    def atualizar(self, dt, fase):
        for e in fase.entidades:
            if isinstance(e, Combatente) and Colisor.verificar(self, e):
                self._coletar(e)
                break

    def _coletar(self, combatente):
        print("Coletado por", combatente.nome)
        combatente.arma = ArmaCanhao()
        self.desativar()

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.COR, (self.x + self.TAMANHO//2, self.y + self.TAMANHO//2), self.TAMANHO//2)