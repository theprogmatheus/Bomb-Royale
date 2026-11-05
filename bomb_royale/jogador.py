import pygame

from .combatente import Combatente
from .configuracoes import COR_JOGADOR, VELOCIDADE_JOGADOR


class Jogador(Combatente):
    def __init__(self, x, y, nome="Jogador"):
        super().__init__(nome, x, y, VELOCIDADE_JOGADOR)
        self._direcao_x = 0
        self._direcao_y = 0

    def processar_input(self):
        teclas = pygame.key.get_pressed()
        self._direcao_x = 0
        self._direcao_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self._direcao_x = -1
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self._direcao_x = 1
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self._direcao_y = -1
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self._direcao_y = 1

    def usar_habilidade(self):
        pass

    def atualizar(self, dt, fase):
        self.processar_input()
        self.mover(self._direcao_x, self._direcao_y, dt, fase)

    def desenhar(self, tela):
        pygame.draw.rect(tela, COR_JOGADOR, self.retangulo)

