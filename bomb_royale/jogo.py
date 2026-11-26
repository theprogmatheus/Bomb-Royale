import pygame

from bomb_royale.colisor import Colisor

from .combatente import Combatente
from .configuracoes import (
    ALTURA_TELA,
    COLUNAS,
    DT_MAXIMO,
    FPS,
    LARGURA_TELA,
    LINHAS,
    TAMANHO_COMBATENTE,
    TITULO,
)
from .fabrica_inimigos import FabricaInimigos
from .fase import Fase
from .hud import HUD
from .jogador import Jogador
from .placar import Placar


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITULO)
        self._tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self._relogio = pygame.time.Clock()
        self._rodando = True
        self._placar = Placar()
        self._hud = HUD()
        self._iniciar_partida()

    def _iniciar_partida(self):
        self._placar.limpar()
        self._partida_encerrada = False
        self._mensagem_fim = ""
        self._fase = Fase()
        self._jogador = self._criar_jogador()
        self._fase.adicionar_entidade(self._jogador)
        # self._fase.adicionar_entidade(self._criar_inimigo())
        self._placar.registrar_combatente(self._jogador.nome)
        inimigo = self._criar_inimigo()
        self._fase.adicionar_entidade(inimigo)
        self._placar.registrar_combatente(inimigo.nome)
        self._teve_rivais = len(self._combatentes_ativos()) > 1

    @property
    def jogador(self):
        return self._jogador

    @property
    def fase(self):
        return self._fase

    @property
    def placar(self):
        return self._placar

    def _criar_jogador(self):
        x, y = Colisor.centro_da_celula(1, 1)
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
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._rodando = False
                elif evento.key == pygame.K_r and self._partida_encerrada:
                    self._iniciar_partida()

    def _combatentes_ativos(self):
        return [e for e in self._fase.entidades if isinstance(e, Combatente) and e.ativo]

    def _verificar_fim_de_partida(self):
        ativos = self._combatentes_ativos()
        if not self._jogador.ativo:
            self._partida_encerrada = True
            self._mensagem_fim = "GAME OVER"
        elif self._teve_rivais and len(ativos) == 1 and ativos[0] is self._jogador:
            self._partida_encerrada = True
            self._mensagem_fim = "VITÓRIA ROYALE!"

    def _atualizar(self, dt):
        if self._partida_encerrada:
            return
        self._fase.atualizar_fase(dt)
        for combatente in self._combatentes_ativos():
            self._placar.sincronizar_combatente(combatente)
        self._verificar_fim_de_partida()

    def _desenhar(self):
        self._fase.desenhar(self._tela)
        self._hud.desenhar(
            self._tela,
            self._jogador,
            self._placar,
            vivos=len(self._combatentes_ativos()),
        )
        if self._partida_encerrada:
            self._hud.desenhar_fim_de_jogo(self._tela, self._mensagem_fim, self._placar)
        pygame.display.flip()

    def loop_principal(self):
        while self._rodando:
            dt = min(self._relogio.tick(FPS) / 1000, DT_MAXIMO)
            self._processar_eventos()
            self._atualizar(dt)
            self._desenhar()
        pygame.quit()

