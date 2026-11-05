from abc import abstractmethod

from .configuracoes import TAMANHO_COMBATENTE, VIDA_INICIAL
from .entidade import Entidade


class Combatente(Entidade):
    def __init__(self, nome, x, y, velocidade):
        super().__init__(x, y, TAMANHO_COMBATENTE, TAMANHO_COMBATENTE)
        self._nome = nome
        self._velocidade = velocidade
        self._vida = VIDA_INICIAL

    @property
    def nome(self):
        return self._nome

    @property
    def velocidade(self):
        return self._velocidade

    @property
    def vida(self):
        return self._vida

    def receber_dano(self, quantidade):
        self._vida = max(0, self._vida - quantidade)
        if self._vida == 0:
            self.desativar()

    def mover(self, direcao_x, direcao_y, dt, fase):
        passo = self._velocidade * dt
        moveu = False

        deslocamento_x = direcao_x * passo
        if deslocamento_x != 0:
            self.x += deslocamento_x
            if fase.colide_com_bloco(self):
                self.x -= deslocamento_x
            else:
                moveu = True

        deslocamento_y = direcao_y * passo
        if deslocamento_y != 0:
            self.y += deslocamento_y
            if fase.colide_com_bloco(self):
                self.y -= deslocamento_y
            else:
                moveu = True

        return moveu

    @abstractmethod
    def usar_habilidade(self):
        pass

