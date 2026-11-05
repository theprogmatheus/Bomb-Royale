import pygame

from .bloco import Bloco
from .colisor import Colisor
from .configuracoes import (
    ALTURA_TELA,
    COLUNAS,
    IMAGEM_FUNDO,
    LARGURA_TELA,
    LINHAS,
    TAMANHO_CELULA,
)


class Fase:
    def __init__(self):
        self._entidades = []
        self._fundo = self._carregar_fundo()
        self._criar_arena()

    @property
    def entidades(self):
        return self._entidades

    @property
    def blocos(self):
        return [e for e in self._entidades if isinstance(e, Bloco)]

    def _carregar_fundo(self):
        imagem = pygame.image.load(IMAGEM_FUNDO).convert()
        escala = max(LARGURA_TELA / imagem.get_width(), ALTURA_TELA / imagem.get_height())
        novo_tamanho = (int(imagem.get_width() * escala) + 1, int(imagem.get_height() * escala) + 1)
        imagem = pygame.transform.smoothscale(imagem, novo_tamanho)
        recorte = pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA)
        recorte.center = imagem.get_rect().center
        return imagem.subsurface(recorte).copy()

    def _criar_arena(self):
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                if self._eh_parede(coluna, linha):
                    x = coluna * TAMANHO_CELULA
                    y = linha * TAMANHO_CELULA
                    self.adicionar_entidade(Bloco(x, y))

    def _eh_parede(self, coluna, linha):
        borda = coluna in (0, COLUNAS - 1) or linha in (0, LINHAS - 1)
        pilar = coluna % 2 == 0 and linha % 2 == 0
        return borda or pilar

    def posicao_na_celula(self, coluna, linha, largura, altura):
        x = coluna * TAMANHO_CELULA + (TAMANHO_CELULA - largura) / 2
        y = linha * TAMANHO_CELULA + (TAMANHO_CELULA - altura) / 2
        return x, y

    def adicionar_entidade(self, entidade):
        self._entidades.append(entidade)

    def remover_entidade(self, entidade):
        self._entidades.remove(entidade)

    def colide_com_bloco(self, entidade):
        return any(Colisor.verificar(entidade, bloco) for bloco in self.blocos)

    def atualizar_fase(self, dt):
        for entidade in list(self._entidades):
            entidade.atualizar(dt, self)
        self._entidades = [e for e in self._entidades if e.ativo]

    def desenhar(self, tela):
        tela.blit(self._fundo, (0, 0))
        for entidade in sorted(self._entidades, key=lambda e: e.retangulo.bottom):
            entidade.desenhar(tela)
