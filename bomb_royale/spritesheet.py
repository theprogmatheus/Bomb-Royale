import pygame

from .configuracoes import (
    ALTURA_SPRITE,
    AREA_MINIMA_RUIDO,
    COLUNAS_SPRITE,
    LINHAS_SPRITE,
    TOLERANCIA_FUNDO,
)


class SpriteSheet:
    def __init__(self, caminho, linhas=LINHAS_SPRITE, colunas=COLUNAS_SPRITE):
        self._linhas = linhas
        self._colunas = colunas
        imagem = pygame.image.load(caminho).convert_alpha()
        mascara_personagem = self._remover_fundo(imagem)
        regioes = self._encontrar_regioes(mascara_personagem, imagem.get_size())
        self._quadros = self._recortar_quadros(imagem, regioes)

    def obter_linha(self, linha):
        return self._quadros[linha]

    @staticmethod
    def espelhar(quadros):
        return [pygame.transform.flip(quadro, True, False) for quadro in quadros]

    def _remover_fundo(self, imagem):
        cor_fundo = imagem.get_at((0, 0))
        tolerancia = (TOLERANCIA_FUNDO, TOLERANCIA_FUNDO, TOLERANCIA_FUNDO, 255)
        pixels_parecidos = pygame.mask.from_threshold(imagem, cor_fundo, tolerancia)
        fundo = pixels_parecidos.connected_component((0, 0))
        fundo.to_surface(imagem, setcolor=(0, 0, 0, 0), unsetcolor=None)
        fundo.invert()
        return fundo

    def _encontrar_regioes(self, mascara_personagem, tamanho_imagem):
        largura, altura = tamanho_imagem
        regioes = {}
        for area in mascara_personagem.get_bounding_rects():
            if area.width * area.height < AREA_MINIMA_RUIDO:
                continue
            linha = area.centery * self._linhas // altura
            coluna = area.centerx * self._colunas // largura
            if (linha, coluna) in regioes:
                regioes[(linha, coluna)] = regioes[(linha, coluna)].union(area)
            else:
                regioes[(linha, coluna)] = area
        return regioes

    def _recortar_quadros(self, imagem, regioes):
        maior_largura = max(area.width for area in regioes.values())
        maior_altura = max(area.height for area in regioes.values())
        escala = ALTURA_SPRITE / maior_altura
        largura_final = int(maior_largura * escala)

        quadros = []
        for linha in range(self._linhas):
            quadros_da_linha = []
            for coluna in range(self._colunas):
                area = regioes[(linha, coluna)]
                recorte = imagem.subsurface(area)
                nova_largura = int(area.width * escala)
                nova_altura = int(area.height * escala)
                recorte = pygame.transform.smoothscale(recorte, (nova_largura, nova_altura))
                quadro = pygame.Surface((largura_final, ALTURA_SPRITE), pygame.SRCALPHA)
                posicao = recorte.get_rect(midbottom=quadro.get_rect().midbottom)
                quadro.blit(recorte, posicao)
                quadros_da_linha.append(quadro)
            quadros.append(quadros_da_linha)
        return quadros

