import random

import pygame

from .bloco import Bloco
from .bomba import Bomba
from .colisor import Colisor
from .configuracoes import (
    ALTURA_TELA,
    CHANCE_BLOCO_DESTRUTIVEL,
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
        return [e for e in self._entidades if isinstance(e, Bloco) and e.ativo]

    @property
    def bombas(self):
        return [e for e in self._entidades if isinstance(e, Bomba) and e.ativo]

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
                x = coluna * TAMANHO_CELULA
                y = linha * TAMANHO_CELULA
                if self._eh_parede(coluna, linha):
                    self.adicionar_entidade(Bloco(x, y))
                elif not self._eh_zona_spawn(coluna, linha) and random.random() < CHANCE_BLOCO_DESTRUTIVEL:
                    self.adicionar_entidade(Bloco(x, y, destrutivel=True))

    def _eh_parede(self, coluna, linha):
        borda = coluna in (0, COLUNAS - 1) or linha in (0, LINHAS - 1)
        pilar = coluna % 2 == 0 and linha % 2 == 0
        return borda or pilar

    def _eh_zona_spawn(self, coluna, linha):
        cantos_livres = {
            (1, 1), (2, 1), (1, 2),
            (COLUNAS - 2, 1), (COLUNAS - 3, 1), (COLUNAS - 2, 2),
            (1, LINHAS - 2), (2, LINHAS - 2), (1, LINHAS - 3),
            (COLUNAS - 2, LINHAS - 2), (COLUNAS - 3, LINHAS - 2), (COLUNAS - 2, LINHAS - 3),
        }
        return (coluna, linha) in cantos_livres

    def posicao_na_celula(self, coluna, linha, largura, altura):
        x = coluna * TAMANHO_CELULA + (TAMANHO_CELULA - largura) / 2
        y = linha * TAMANHO_CELULA + (TAMANHO_CELULA - altura) / 2
        return x, y

    def adicionar_entidade(self, entidade):
        self._entidades.append(entidade)

    def remover_entidade(self, entidade):
        if entidade in self._entidades:
            self._entidades.remove(entidade)

    # Função para obeter as entidades que ocupa a célula
    def obter_entidades(self, coluna, linha):
        entidades = []
        for entidade in self.entidades:
            coluna_e, linha_e = Colisor.obter_celula_grid(entidade.x, entidade.y)
            if (coluna_e == coluna and linha_e == linha):
                entidades.append(entidade)
        return entidades

    def colide_com_bloco(self, entidade):
        return any(Colisor.verificar(entidade, bloco) for bloco in self.blocos)

    def colide_com_obstaculo(self, entidade, ignorar=()):
        if self.colide_com_bloco(entidade):
            return True
        return any(
            Colisor.verificar(entidade, bomba)
            for bomba in self.bombas
            if bomba not in ignorar
        )

    def atualizar_fase(self, dt):
        for entidade in list(self._entidades):
            entidade.atualizar(dt, self)
        self._entidades = [e for e in self._entidades if e.ativo]

    def desenhar(self, tela):
        tela.blit(self._fundo, (0, 0))
        for entidade in sorted(self._entidades, key=lambda e: e.retangulo.bottom):
            entidade.desenhar(tela)
