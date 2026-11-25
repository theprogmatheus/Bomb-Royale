# =============================================================================
# CÓDIGO GERADO POR INTELIGÊNCIA ARTIFICIAL
# Autor: Claude Sonnet 5.5 (Anthropic), via Claude Code, em 25/11/2026.
# Todo o conteúdo deste arquivo foi escrito pela IA.
# =============================================================================
#
# Recorta o assets/explosion.jpg (2400x1792) nas peças da explosão em cruz:
#   obter_linha(0): centro
#   obter_linha(1): trecho reto (horizontal)
#   obter_linha(2): ponta virada para a direita
# Cada linha tem 4 quadros de animação. As outras direções saem girando a peça
# com pygame.transform.rotate. Desenhe cada peça centralizada na célula, porque
# a ponta é mais alta que ela.

import pygame

from .configuracoes import TAMANHO_CELULA
from .spritesheet import SpriteSheet


class SpriteSheetExplosao(SpriteSheet):
    TOLERANCIA = 100

    # Lado, em pixels da imagem, do pedaço que vira uma célula do jogo.
    LADO = 220
    ALTURA_PONTA = 480

    # Canto superior esquerdo de cada quadro dentro da imagem.
    CENTROS = [(190, 186), (790, 186), (1390, 186), (1990, 186)]
    TRECHOS = [(190, 794), (790, 786), (1390, 786), (1990, 794)]
    PONTAS = [(320, 1256), (937, 1256), (1522, 1256), (2124, 1256)]

    def _remover_fundo(self, imagem):
        # Apaga todo pixel parecido com o fundo, e não só os ligados ao canto:
        # a imagem tem linhas de grade fracas que isolam partes do verde.
        cor_fundo = imagem.get_at((0, 0))
        tolerancia = (self.TOLERANCIA, self.TOLERANCIA, self.TOLERANCIA, 255)
        fundo = pygame.mask.from_threshold(imagem, cor_fundo, tolerancia)
        fundo.to_surface(imagem, setcolor=(0, 0, 0, 0), unsetcolor=None)
        fundo.invert()
        return fundo

    def _recortar_quadros(self, imagem, regioes):
        # As posições são fixas, então as regiões detectadas não são usadas.
        centros = [self._recortar_peca(imagem, x, y, self.LADO) for x, y in self.CENTROS]
        trechos = [self._recortar_peca(imagem, x, y, self.LADO) for x, y in self.TRECHOS]
        pontas = [self._recortar_peca(imagem, x, y, self.ALTURA_PONTA) for x, y in self.PONTAS]
        return [centros, trechos, pontas]

    def _recortar_peca(self, imagem, x, y, altura):
        escala = TAMANHO_CELULA / self.LADO
        area = pygame.Rect(x, y, self.LADO, altura)
        tamanho = (TAMANHO_CELULA, round(altura * escala))
        return pygame.transform.scale(imagem.subsurface(area), tamanho)
