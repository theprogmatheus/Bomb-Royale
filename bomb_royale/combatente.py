from abc import abstractmethod

import pygame

from .animacao import Animacao
from .configuracoes import TAMANHO_CELULA, TAMANHO_COMBATENTE, TOLERANCIA_QUINA, VIDA_INICIAL, DEBUG_MODE
from .entidade import Entidade
from .spritesheet import SpriteSheet
from .arma_bomba import ArmaBomba
from .colisor import Colisor


class Combatente(Entidade):
    LINHA_BAIXO = 0
    LINHA_CIMA = 1
    LINHA_LADO = 2

    def __init__(self, nome, x, y, velocidade, caminho_sprite):
        super().__init__(x, y, TAMANHO_COMBATENTE, TAMANHO_COMBATENTE)
        self._nome = nome
        self._velocidade = velocidade
        self._vida = VIDA_INICIAL
        self._animacoes = self._criar_animacoes(caminho_sprite)
        self._direcao_visual = "baixo"
        self._movendo = False
        self._arma = ArmaBomba(2)
        self._pontuacao = 0

    @property
    def nome(self):
        return self._nome

    @property
    def velocidade(self):
        return self._velocidade

    @property
    def vida(self):
        return self._vida
    
    @property
    def arma(self):
        return self._arma
    
    @arma.setter
    def arma(self, nova_arma):
        self._arma = nova_arma
        
    @property
    def pontuacao(self):
        return self._pontuacao
    
    @pontuacao.setter
    def pontuacao(self, nova_pontuacao):
        if (nova_pontuacao < 0):
            nova_pontuacao = 0
        self._pontuacao = nova_pontuacao

    def _criar_animacoes(self, caminho_sprite):
        sprite_sheet = SpriteSheet(caminho_sprite)
        lado_direito = sprite_sheet.obter_linha(self.LINHA_LADO)
        return {
            "baixo": Animacao(sprite_sheet.obter_linha(self.LINHA_BAIXO)),
            "cima": Animacao(sprite_sheet.obter_linha(self.LINHA_CIMA)),
            "direita": Animacao(lado_direito),
            "esquerda": Animacao(SpriteSheet.espelhar(lado_direito)),
        }

    def receber_dano(self, quantidade):
        self._vida = max(0, self._vida - quantidade)
        if self._vida == 0:
            self.desativar()

    def _atualizar_direcao_visual(self, direcao_x, direcao_y):
        if direcao_x > 0:
            self._direcao_visual = "direita"
        elif direcao_x < 0:
            self._direcao_visual = "esquerda"
        elif direcao_y > 0:
            self._direcao_visual = "baixo"
        elif direcao_y < 0:
            self._direcao_visual = "cima"

    def _atualizar_animacao(self, dt):
        animacao = self._animacoes[self._direcao_visual]
        if self._movendo:
            animacao.atualizar(dt)
        else:
            animacao.reiniciar()

    def _colide_deslocado(self, deslocamento_x, deslocamento_y, fase):
        self.x += deslocamento_x
        self.y += deslocamento_y
        colidiu = fase.colide_com_bloco(self)
        self.x -= deslocamento_x
        self.y -= deslocamento_y
        return colidiu

    def _tentar_mover(self, deslocamento_x, deslocamento_y, fase):
        if deslocamento_x == 0 and deslocamento_y == 0:
            return False
        if self._colide_deslocado(deslocamento_x, deslocamento_y, fase):
            return False
        self.x += deslocamento_x
        self.y += deslocamento_y
        return True

    def _deslizar_na_quina(self, direcao_x, direcao_y, passo, fase):
        lateral_x, lateral_y = (0, 1) if direcao_x != 0 else (1, 0)
        for distancia in range(1, TOLERANCIA_QUINA + 1):
            for sentido in (-1, 1):
                ajuste_x = lateral_x * sentido * distancia
                ajuste_y = lateral_y * sentido * distancia
                caminho_livre = not self._colide_deslocado(
                    ajuste_x + direcao_x * passo, ajuste_y + direcao_y * passo, fase
                )
                posicao_livre = not self._colide_deslocado(ajuste_x, ajuste_y, fase)
                if caminho_livre and posicao_livre:
                    deslize = min(passo, distancia) * sentido
                    return self._tentar_mover(lateral_x * deslize, lateral_y * deslize, fase)
        return False
    
    @property
    def retangulo(self):
        return pygame.Rect(self.x - (self.largura / 2), self.y - (self.altura / 2), self._largura, self._altura)

    def mover(self, direcao_x, direcao_y, dt, fase):
        self._atualizar_direcao_visual(direcao_x, direcao_y)
        passo = self._velocidade * dt

        moveu_x = self._tentar_mover(direcao_x * passo, 0, fase)
        moveu_y = self._tentar_mover(0, direcao_y * passo, fase)
        moveu = moveu_x or moveu_y

        if not moveu and (direcao_x != 0 or direcao_y != 0):
            moveu = self._deslizar_na_quina(direcao_x, direcao_y, passo, fase)

        self._movendo = moveu
        return moveu

    def desenhar(self, tela):
        quadro = self._animacoes[self._direcao_visual].quadro_atual
        posicao = quadro.get_rect(center=(self.x, self.y)) # Centraliza o quadro na posição do combatente
        tela.blit(quadro, posicao)
        
        if (DEBUG_MODE):
            coluna, linha = Colisor.obter_celula_grid(self.x, self.y)
            
            # Desenhar retângulo na celula em que o jogador está
            pygame.draw.rect(tela, (255, 0, 0), (coluna * TAMANHO_CELULA, linha * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 1) 
            
            # Desenha um retângulo ao redor do combatente para depuração
            pygame.draw.rect(tela, (0, 255, 0), self.retangulo, 1)
            
            #Desenha um ponto no x e y exato do combatente para depuração
            pygame.draw.circle(tela, (0, 0, 255), (int(self.x), int(self.y)), 3)
            
            print(f"X={self.x}, Y={self.y}, Coluna={coluna}, Linha={linha} Posicao={posicao}")
            
    @abstractmethod
    def usar_habilidade(self, fase):
        pass
