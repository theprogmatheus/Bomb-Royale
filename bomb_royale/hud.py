import pygame

from .configuracoes import ALTURA_TELA, LARGURA_TELA


class HUD:
    ALTURA_BARRA = 42
    MARGEM_X = 8
    MARGEM_Y = 5

    # Paleta rústica 16-bit (Bomberman / SNES old school)
    COR_PRETO = (20, 16, 14)
    COR_MADEIRA_ESCURA = (56, 40, 29)
    COR_MADEIRA_MEDIA = (84, 59, 41)
    COR_MADEIRA_CLARA = (132, 95, 64)
    COR_BEVEL_TOPO = (176, 134, 88)
    COR_PAINEL_FUNDO = (30, 24, 21)
    COR_PAINEL_BORDA = (104, 77, 54)
    COR_REBITE = (164, 152, 136)

    COR_CREME = (255, 244, 214)
    COR_AMARELO = (255, 210, 64)
    COR_LARANJA = (232, 122, 42)
    COR_VERMELHO = (224, 56, 56)
    COR_CIANO = (92, 224, 255)
    COR_PRATA = (206, 212, 220)
    COR_BRONZE = (212, 146, 86)
    COR_OVERLAY = (14, 10, 8, 195)

    NOMES_ARMAS = {
        "ArmaBomba": "BOMBA",
        "ArmaCanhao": "CANHÃO",
    }

    # Sprites pixel-art (desenhados em blocos 2x2)
    SPRITE_CORACAO_CHEIO = [
        "..KKK...KKK..",
        ".KRRRK.KRRRK.",
        "KRWWRRKRKRRRK",
        "KRWRRRRRRRRRK",
        "KRRRRRRRRRRRK",
        ".KRRRRRRRRRK.",
        "..KRRRRRRRK..",
        "...KRRRRRK...",
        "....KRRRK....",
        ".....KRK.....",
        "......K......",
    ]

    SPRITE_CORACAO_VAZIO = [
        "..KKK...KKK..",
        ".KDDDK.KDDDK.",
        "KDDDDDKDDDDDK",
        "KDDDDDDDDDDDK",
        "KDDDDDDDDDDDK",
        ".KDDDDDDDDDK.",
        "..KDDDDDDDK..",
        "...KDDDDDK...",
        "....KDDDK....",
        ".....KDK.....",
        "......K......",
    ]

    SPRITE_MOEDA = [
        "..KKKKK..",
        ".KYYYYYK.",
        "KYWWYOOYK",
        "KYWYYOOYK",
        "KYWYYOOYK",
        "KYWYYOOYK",
        "KYYYYOOYK",
        ".KOOOOOK.",
        "..KKKKK..",
    ]

    SPRITE_BOMBA = [
        "........FY.",
        ".......OFF.",
        "......KK...",
        "...KKKKKK..",
        "..KBBBBBBK.",
        ".KBWWBBBBBK",
        ".KBWBBBBBBK",
        ".KBBBBBBBBK",
        ".KBBBBBBBBK",
        "..KBBBBBBK.",
        "...KKKKKK..",
    ]

    SPRITE_CANHAO = [
        "....KKKKKK...",
        "..KKCCCCCCKK.",
        ".KCCWWWWCCCCK",
        "KCCCCCCCCCCCK",
        "KCCSSSSSSCCCK",
        ".KKCCCCCCKK..",
        "...KKKKKK....",
    ]

    SPRITE_BOMBER = [
        "....KK....",
        "...KYYK...",
        "..KKKKKK..",
        ".KWWWWWWK.",
        "KWKCCCCKWK",
        "KWKCKKCKWK",
        "KWKCCCCKWK",
        ".KWWWWWWK.",
        "..KKKKKK..",
    ]

    PALETA_PIXELS = {
        "K": (20, 16, 14),
        "R": (228, 52, 52),
        "W": (255, 250, 238),
        "D": (66, 54, 48),
        "Y": (255, 214, 66),
        "O": (214, 130, 36),
        "F": (255, 118, 36),
        "B": (46, 54, 72),
        "C": (82, 216, 255),
        "S": (52, 128, 178),
    }

    def __init__(self):
        self._fonte_valor = pygame.font.SysFont("consolas", 18, bold=True)
        self._fonte_rotulo = pygame.font.SysFont("consolas", 12, bold=True)
        self._fonte_titulo = pygame.font.SysFont("consolas", 36, bold=True)
        self._fonte_ranking = pygame.font.SysFont("consolas", 19, bold=True)
        self._barra_base = self._criar_barra_rustica()

    def _desenhar_pixel_art(self, tela, matriz, x, y, escala=2):
        for linha_idx, linha in enumerate(matriz):
            for col_idx, simbolo in enumerate(linha):
                cor = self.PALETA_PIXELS.get(simbolo)
                if cor is not None:
                    pygame.draw.rect(
                        tela,
                        cor,
                        (x + col_idx * escala, y + linha_idx * escala, escala, escala),
                    )

    def _desenhar_caixa_retro(self, tela, x, y, w, h, fundo=None, bevel=True):
        cor_fundo = fundo if fundo is not None else self.COR_PAINEL_FUNDO
        pygame.draw.rect(tela, cor_fundo, (x, y, w, h))
        if bevel:
            # Efeito rebaixado 16-bit (escuro em cima/esq, claro embaixo/dir)
            pygame.draw.line(tela, self.COR_PRETO, (x, y), (x + w - 1, y), 2)
            pygame.draw.line(tela, self.COR_PRETO, (x, y), (x, y + h - 1), 2)
            pygame.draw.line(tela, self.COR_PAINEL_BORDA, (x, y + h - 1), (x + w - 1, y + h - 1), 2)
            pygame.draw.line(tela, self.COR_PAINEL_BORDA, (x + w - 1, y), (x + w - 1, y + h - 1), 2)
        else:
            pygame.draw.rect(tela, self.COR_PRETO, (x, y, w, h), 2)

    def _criar_barra_rustica(self):
        largura = LARGURA_TELA - self.MARGEM_X * 2
        altura = self.ALTURA_BARRA
        surf = pygame.Surface((largura, altura + 3), pygame.SRCALPHA)

        # Sombra dura pixelada embaixo
        pygame.draw.rect(surf, (0, 0, 0, 120), (3, 3, largura - 3, altura))

        # Base de madeira/pedra rústica com tábuas sutis
        pygame.draw.rect(surf, self.COR_MADEIRA_MEDIA, (0, 0, largura, altura))
        for y in range(4, altura - 4, 6):
            pygame.draw.line(surf, self.COR_MADEIRA_ESCURA, (4, y), (largura - 5, y), 1)

        # Moldura chanfrada 16-bit (luz no topo/esq, sombra embaixo/dir)
        pygame.draw.rect(surf, self.COR_PRETO, (0, 0, largura, altura), 2)
        pygame.draw.line(surf, self.COR_BEVEL_TOPO, (2, 2), (largura - 3, 2), 2)
        pygame.draw.line(surf, self.COR_BEVEL_TOPO, (2, 2), (2, altura - 3), 2)
        pygame.draw.line(surf, self.COR_MADEIRA_ESCURA, (2, altura - 3), (largura - 3, altura - 3), 2)
        pygame.draw.line(surf, self.COR_MADEIRA_ESCURA, (largura - 3, 2), (largura - 3, altura - 3), 2)

        # 4 rebites de ferro nos cantos
        for rx, ry in [(6, 6), (largura - 10, 6), (6, altura - 10), (largura - 10, altura - 10)]:
            pygame.draw.rect(surf, self.COR_PRETO, (rx, ry, 4, 4))
            pygame.draw.rect(surf, self.COR_REBITE, (rx, ry, 2, 2))

        return surf

    def _desenhar_texto_retro(self, tela, fonte, texto, cor, x, y, centralizado=False, alinhar_centro_y=False):
        # antialias=False + sombra dura 2px = cara autêntica de jogo 16-bit
        sombra = fonte.render(texto, False, self.COR_PRETO)
        principal = fonte.render(texto, False, cor)
        if centralizado:
            rect = principal.get_rect(center=(x, y))
        elif alinhar_centro_y:
            rect = principal.get_rect(midleft=(x, y))
        else:
            rect = principal.get_rect(topleft=(x, y))
        tela.blit(sombra, (rect.x + 2, rect.y + 2))
        tela.blit(principal, rect)
        return rect

    def _info_arma(self, jogador):
        arma = getattr(jogador, "arma", None)
        if arma is None:
            return "BOMBA", "∞", None, False

        nome_classe = type(arma).__name__
        nome_exibicao = self.NOMES_ARMAS.get(nome_classe, nome_classe.upper())
        municao = getattr(arma, "municao", None)
        texto_municao = "∞" if municao is None else str(municao)
        tempo_restante = getattr(arma, "tempo_restante", None)
        eh_canhao = "Canhao" in nome_classe
        return nome_exibicao, texto_municao, tempo_restante, eh_canhao

    def desenhar(self, tela, jogador, placar, vivos=None):
        tela.blit(self._barra_base, (self.MARGEM_X, self.MARGEM_Y))
        centro_y = self.MARGEM_Y + self.ALTURA_BARRA // 2
        caixa_y = self.MARGEM_Y + 7
        caixa_h = self.ALTURA_BARRA - 14

        total_vidas = max(3, jogador.vida)
        w_vida = 18 + total_vidas * 30
        w_pontos = 152
        nome_arma, texto_municao, tempo_restante, eh_canhao = self._info_arma(jogador)
        w_arma = 228 if tempo_restante is not None else 188
        w_vivos = 98 if vivos is not None else 0

        margem_interna = self.MARGEM_X + 18
        largura_util = LARGURA_TELA - margem_interna * 2
        larguras = [w_vida, w_pontos, w_arma] + ([w_vivos] if vivos is not None else [])
        espaco = max(10, (largura_util - sum(larguras)) // max(1, len(larguras) - 1))

        # 1. Vidas (corações pixel-art)
        x_vida = margem_interna
        self._desenhar_caixa_retro(tela, x_vida, caixa_y, w_vida, caixa_h)
        for indice in range(total_vidas):
            sprite = self.SPRITE_CORACAO_CHEIO if indice < jogador.vida else self.SPRITE_CORACAO_VAZIO
            sx = x_vida + 11 + indice * 30
            sy = centro_y - (len(sprite) * 2) // 2
            self._desenhar_pixel_art(tela, sprite, sx, sy, escala=2)

        # 2. Pontuação arcade (moeda pixel + placar 6 dígitos)
        pontos = placar.obter_pontos(jogador.nome)
        x_pontos = x_vida + w_vida + espaco
        self._desenhar_caixa_retro(tela, x_pontos, caixa_y, w_pontos, caixa_h)
        self._desenhar_pixel_art(
            tela, self.SPRITE_MOEDA, x_pontos + 10, centro_y - (len(self.SPRITE_MOEDA) * 2) // 2, escala=2
        )
        self._desenhar_texto_retro(
            tela,
            self._fonte_valor,
            f"{pontos:06d}",
            self.COR_AMARELO,
            x_pontos + 38,
            centro_y + 1,
            alinhar_centro_y=True,
        )

        # 3. Arma equipada (bomba ou canhão pixel-art)
        x_arma = x_pontos + w_pontos + espaco
        self._desenhar_caixa_retro(tela, x_arma, caixa_y, w_arma, caixa_h)
        sprite_arma = self.SPRITE_CANHAO if eh_canhao else self.SPRITE_BOMBA
        self._desenhar_pixel_art(
            tela, sprite_arma, x_arma + 8, centro_y - (len(sprite_arma) * 2) // 2, escala=2
        )
        cor_arma = self.COR_CIANO if eh_canhao else self.COR_CREME
        texto_arma = f"{nome_arma} x{texto_municao}"
        if tempo_restante is not None:
            texto_arma += f" {int(tempo_restante)}s"
        self._desenhar_texto_retro(
            tela, self._fonte_valor, texto_arma, cor_arma, x_arma + 38, centro_y + 1, alinhar_centro_y=True
        )

        # 4. Sobreviventes (mini bomber pixel + xN)
        if vivos is not None:
            x_vivos = LARGURA_TELA - margem_interna - w_vivos
            self._desenhar_caixa_retro(tela, x_vivos, caixa_y, w_vivos, caixa_h)
            self._desenhar_pixel_art(
                tela, self.SPRITE_BOMBER, x_vivos + 10, centro_y - (len(self.SPRITE_BOMBER) * 2) // 2, escala=2
            )
            self._desenhar_texto_retro(
                tela, self._fonte_valor, f"x{vivos}", self.COR_CREME, x_vivos + 40, centro_y + 1, alinhar_centro_y=True
            )

    def desenhar_fim_de_jogo(self, tela, titulo, placar):
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill(self.COR_OVERLAY)
        tela.blit(overlay, (0, 0))

        eh_vitoria = "VITÓRIA" in titulo.upper()
        cor_titulo = self.COR_AMARELO if eh_vitoria else self.COR_VERMELHO

        ranking = placar.obter_ranking()
        w_card = 490
        h_card = max(310, 225 + len(ranking) * 42)
        card_x = (LARGURA_TELA - w_card) // 2
        card_y = (ALTURA_TELA - h_card) // 2

        # Sombra pixelada do card
        pygame.draw.rect(tela, (0, 0, 0), (card_x + 6, card_y + 6, w_card, h_card))

        # Moldura de madeira/pedra 16-bit
        pygame.draw.rect(tela, self.COR_MADEIRA_MEDIA, (card_x, card_y, w_card, h_card))
        pygame.draw.rect(tela, self.COR_PRETO, (card_x, card_y, w_card, h_card), 3)
        pygame.draw.line(tela, self.COR_BEVEL_TOPO, (card_x + 3, card_y + 3), (card_x + w_card - 4, card_y + 3), 3)
        pygame.draw.line(tela, self.COR_BEVEL_TOPO, (card_x + 3, card_y + 3), (card_x + 3, card_y + h_card - 4), 3)
        pygame.draw.line(
            tela,
            self.COR_MADEIRA_ESCURA,
            (card_x + 3, card_y + h_card - 4),
            (card_x + w_card - 4, card_y + h_card - 4),
            3,
        )
        pygame.draw.line(
            tela,
            self.COR_MADEIRA_ESCURA,
            (card_x + w_card - 4, card_y + 3),
            (card_x + w_card - 4, card_y + h_card - 4),
            3,
        )

        # Painel interno escuro
        self._desenhar_caixa_retro(tela, card_x + 18, card_y + 18, w_card - 36, h_card - 36)

        # Rebites nos 4 cantos
        for rx, ry in [
            (card_x + 8, card_y + 8),
            (card_x + w_card - 14, card_y + 8),
            (card_x + 8, card_y + h_card - 14),
            (card_x + w_card - 14, card_y + h_card - 14),
        ]:
            pygame.draw.rect(tela, self.COR_PRETO, (rx, ry, 6, 6))
            pygame.draw.rect(tela, self.COR_REBITE, (rx, ry, 3, 3))

        # Título arcade
        self._desenhar_texto_retro(
            tela, self._fonte_titulo, titulo.upper(), cor_titulo, LARGURA_TELA // 2, card_y + 62, centralizado=True
        )
        self._desenhar_texto_retro(
            tela,
            self._fonte_rotulo,
            "=== PLACAR DA ARENA ===",
            self.COR_BEVEL_TOPO,
            LARGURA_TELA // 2,
            card_y + 104,
            centralizado=True,
        )

        cores_podio = [self.COR_AMARELO, self.COR_PRATA, self.COR_BRONZE]
        rotulos_pos = ["1ST", "2ND", "3RD"]
        y_linha = card_y + 144
        for indice, registro in enumerate(ranking):
            cor_linha = cores_podio[indice] if indice < len(cores_podio) else self.COR_CREME
            pos_txt = rotulos_pos[indice] if indice < len(rotulos_pos) else f"{indice + 1}TH"
            self._desenhar_caixa_retro(
                tela, card_x + 42, y_linha - 16, w_card - 84, 34, fundo=self.COR_MADEIRA_ESCURA, bevel=False
            )
            self._desenhar_texto_retro(
                tela,
                self._fonte_ranking,
                f"{pos_txt}  {registro}",
                cor_linha,
                LARGURA_TELA // 2,
                y_linha + 1,
                centralizado=True,
            )
            y_linha += 42

        self._desenhar_texto_retro(
            tela,
            self._fonte_rotulo,
            "[R] JOGAR DE NOVO    |    [ESC] SAIR",
            self.COR_CREME,
            LARGURA_TELA // 2,
            card_y + h_card - 36,
            centralizado=True,
        )
