import pygame

from .combatente import Combatente
from .configuracoes import SPRITE_JOGADOR, VELOCIDADE_JOGADOR


class Jogador(Combatente):
    def __init__(self, x, y, nome="Jogador"):
        super().__init__(nome, x, y, VELOCIDADE_JOGADOR, SPRITE_JOGADOR)
        self._direcao_x = 0
        self._direcao_y = 0

    def processar_input(self, fase):
        teclas = pygame.key.get_pressed()
        self._direcao_x = 0
        self._direcao_y = 0      

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self._direcao_x = -1
            
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self._direcao_x = 1
            
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self._direcao_y = -1
            
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self._direcao_y = 1
            
        if teclas[pygame.K_SPACE]:
            self.arma.disparar(self, fase)
            
        if teclas[pygame.K_e]:
            self.usar_habilidade(fase)

    def usar_habilidade(self, fase):
        pass

    def atualizar(self, dt, fase):
        self.processar_input(fase)
        self.mover(self._direcao_x, self._direcao_y, dt, fase)
        self._atualizar_animacao(dt)
