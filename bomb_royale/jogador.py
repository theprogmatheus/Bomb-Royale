import pygame

from .combatente import Combatente
from .configuracoes import SPRITE_JOGADOR, VELOCIDADE_JOGADOR


class Jogador(Combatente):
    def __init__(self, x, y, nome="Jogador"):
        super().__init__(nome, x, y, VELOCIDADE_JOGADOR, SPRITE_JOGADOR)
        self._direcao_x = 0
        self._direcao_y = 0

    def processar_input(self):
        teclas = pygame.key.get_pressed()
        self._direcao_x = 0
        self._direcao_y = 0

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self._direcao_x = -1
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self._direcao_x = 1
        elif teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self._direcao_y = -1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self._direcao_y = 1

    def usar_habilidade(self):
        pass

    def atualizar(self, dt, fase):
        self.processar_input()
        self.mover(self._direcao_x, self._direcao_y, dt, fase)
        self._atualizar_animacao(dt)
