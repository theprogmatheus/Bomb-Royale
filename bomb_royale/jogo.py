import pygame

from .configuracoes import (
    ALTURA_TELA,
    COLUNAS,
    FPS,
    LARGURA_TELA,
    LINHAS,
    TAMANHO_COMBATENTE,
    TITULO,
)
from .fabrica_inimigos import FabricaInimigos
from .fase import Fase
from .jogador import Jogador


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITULO)
        self._tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self._relogio = pygame.time.Clock()
        self._rodando = True
        self._fase = Fase()
        self._jogador = self._criar_jogador()
        self._fase.adicionar_entidade(self._jogador)
        self._fase.adicionar_entidade(self._criar_inimigo())

    @property
    def jogador(self):
        return self._jogador

    @property
    def fase(self):
        return self._fase

    def _criar_jogador(self):
        x, y = self._fase.posicao_na_celula(1, 1, TAMANHO_COMBATENTE, TAMANHO_COMBATENTE)
        return Jogador(x, y)

    def _criar_inimigo(self):
        x, y = self._fase.posicao_na_celula(
            COLUNAS - 2, LINHAS - 2, TAMANHO_COMBATENTE, TAMANHO_COMBATENTE
        )
        return FabricaInimigos.criar("builder", x, y)

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self._rodando = False

    def _atualizar(self, dt):
        self._fase.atualizar_fase(dt)

    def _desenhar(self):
        self._fase.desenhar(self._tela)
        pygame.display.flip()

    def loop_principal(self):
        while self._rodando:
            dt = self._relogio.tick(FPS) / 1000
            self._processar_eventos()
            self._atualizar(dt)
            self._desenhar()
        pygame.quit()

