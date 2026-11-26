import pygame

from .configuracoes import ALTURA_TELA, LARGURA_TELA, TAMANHO_CELULA


class HUD:
    COR_FUNDO_BARRA = (20, 24, 34, 215)
    COR_BORDA_BARRA = (85, 95, 115)
    COR_TEXTO = (245, 247, 250)
    COR_DESTAQUE = (255, 210, 70)
    COR_VIDA_ATIVA = (230, 65, 65)
    COR_VIDA_PERDIDA = (80, 80, 90)
    COR_OVERLAY = (10, 12, 18, 195)

    NOMES_ARMAS = {
        "ArmaBomba": "Bomba",
        "ArmaCanhao": "Canhão",
    }

    def __init__(self):
        self._fonte_padrao = pygame.font.SysFont("segoeui", 19, bold=True)
        self._fonte_titulo = pygame.font.SysFont("segoeui", 40, bold=True)
        self._fonte_subtitulo = pygame.font.SysFont("segoeui", 22)

    def _formatar_arma(self, jogador):
        arma = getattr(jogador, "arma", None)
        if arma is None:
            return "Arma: Bomba (∞)"

        nome_classe = type(arma).__name__
        nome_exibicao = self.NOMES_ARMAS.get(nome_classe, nome_classe)
        municao = getattr(arma, "municao", None)
        texto_municao = "∞" if municao is None else str(municao)
        tempo_restante = getattr(arma, "tempo_restante", None)
        if tempo_restante is not None:
            return f"Arma: {nome_exibicao} ({texto_municao}) [{int(tempo_restante)}s]"
        return f"Arma: {nome_exibicao} ({texto_municao})"

    def _desenhar_barra_fundo(self, tela):
        altura_barra = TAMANHO_CELULA - 12
        barra = pygame.Surface((LARGURA_TELA - 16, altura_barra), pygame.SRCALPHA)
        barra.fill(self.COR_FUNDO_BARRA)
        pygame.draw.rect(barra, self.COR_BORDA_BARRA, barra.get_rect(), width=1, border_radius=8)
        tela.blit(barra, (8, 6))
        return 6 + altura_barra // 2

    def _desenhar_vidas(self, tela, vida_atual, centro_y):
        rotulo = self._fonte_padrao.render("Vida:", True, self.COR_TEXTO)
        tela.blit(rotulo, (22, centro_y - rotulo.get_height() // 2))

        total_blocos = max(3, vida_atual)
        x_inicial = 22 + rotulo.get_width() + 10
        for indice in range(total_blocos):
            cor = self.COR_VIDA_ATIVA if indice < vida_atual else self.COR_VIDA_PERDIDA
            retangulo = pygame.Rect(x_inicial + indice * 22, centro_y - 8, 16, 16)
            pygame.draw.rect(tela, cor, retangulo, border_radius=4)

    def desenhar(self, tela, jogador, placar, vivos=None):
        centro_y = self._desenhar_barra_fundo(tela)
        self._desenhar_vidas(tela, jogador.vida, centro_y)

        pontos = placar.obter_pontos(jogador.nome)
        texto_pontos = self._fonte_padrao.render(f"Pontos: {pontos}", True, self.COR_DESTAQUE)
        tela.blit(texto_pontos, (220, centro_y - texto_pontos.get_height() // 2))

        texto_arma = self._fonte_padrao.render(self._formatar_arma(jogador), True, self.COR_TEXTO)
        tela.blit(texto_arma, (410, centro_y - texto_arma.get_height() // 2))

        if vivos is not None:
            texto_vivos = self._fonte_padrao.render(f"Vivos: {vivos}", True, self.COR_TEXTO)
            x_vivos = LARGURA_TELA - texto_vivos.get_width() - 24
            tela.blit(texto_vivos, (x_vivos, centro_y - texto_vivos.get_height() // 2))

    def desenhar_fim_de_jogo(self, tela, titulo, placar):
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill(self.COR_OVERLAY)
        tela.blit(overlay, (0, 0))

        superficie_titulo = self._fonte_titulo.render(titulo, True, self.COR_DESTAQUE)
        rect_titulo = superficie_titulo.get_rect(center=(LARGURA_TELA // 2, 160))
        tela.blit(superficie_titulo, rect_titulo)

        subtitulo = self._fonte_subtitulo.render("Ranking da Partida", True, self.COR_TEXTO)
        rect_sub = subtitulo.get_rect(center=(LARGURA_TELA // 2, 225))
        tela.blit(subtitulo, rect_sub)

        y_linha = 275
        for posicao, registro in enumerate(placar.obter_ranking(), start=1):
            linha = self._fonte_subtitulo.render(f"{posicao}. {registro}", True, self.COR_TEXTO)
            rect_linha = linha.get_rect(center=(LARGURA_TELA // 2, y_linha))
            tela.blit(linha, rect_linha)
            y_linha += 36

        dica = self._fonte_padrao.render(
            "Pressione R para reiniciar ou ESC para sair", True, self.COR_BORDA_BARRA
        )
        rect_dica = dica.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 90))
        tela.blit(dica, rect_dica)
