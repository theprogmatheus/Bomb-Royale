from bomb_royale.animacao import Animacao

from .entidade import Entidade
from .configuracoes import SPRITE_ENTITY_EXPLOSION
from .spritesheet_explosao import SpritesheetExplosao
from .colisor import Colisor
from .bloco import Bloco

import pygame

class Explosao(Entidade):

    LARGURA = 36
    ALTURA = 36
    QUADROS = None

    def __init__(self, bomba, x, y, raio):
        super().__init__(x, y, self.LARGURA, self.ALTURA)
        self.__bomba = bomba
        self.__raio = raio
        self.__celulas = [] # (coluna, linha, tipo, angulo)
        self.__lifetime = 0.4
         
        quadros = self.carregar_quadros()
        self.__animacoes = {
            ("centro", -1): Animacao(quadros["centro"], 0.1),
            ("lado", 0): Animacao(quadros["lado_h"], 0.1),
            ("lado", 1): Animacao(quadros["lado_v"], 0.1),
            ("lado", 2): Animacao(quadros["lado_h"], 0.1),
            ("lado", 3): Animacao(quadros["lado_v"], 0.1),
            ("ponta", 0): Animacao(quadros["ponta_esq"], 0.1),
            ("ponta", 1): Animacao(quadros["ponta_cima"], 0.1),
            ("ponta", 2): Animacao(quadros["ponta_dir"], 0.1),
            ("ponta", 3): Animacao(quadros["ponta_baixo"], 0.1),
        }
    
    @classmethod
    def carregar_quadros(cls):
        if (cls.QUADROS is None):
            
            sprite_sheet = SpritesheetExplosao(SPRITE_ENTITY_EXPLOSION, 3, 4)              
            quadros_lado = sprite_sheet.obter_linha(1)
            quadros_ponta = sprite_sheet.obter_linha(2)
            
            cls.QUADROS = {
                "centro": sprite_sheet.obter_linha(0),
                "lado_h": quadros_lado,
                "lado_v": [],
                "ponta_esq": [],
                "ponta_cima": [],
                "ponta_dir": [],
                "ponta_baixo": []
            }

            cls.QUADROS["lado_v"] = [pygame.transform.rotate(quadro, 90) for quadro in quadros_lado]
            cls.QUADROS["ponta_esq"] = [pygame.transform.rotate(quadro, 180) for quadro in quadros_ponta]
            cls.QUADROS["ponta_cima"] = [pygame.transform.rotate(quadro, 90) for quadro in quadros_ponta]
            cls.QUADROS["ponta_dir"] = [pygame.transform.rotate(quadro, 0) for quadro in quadros_ponta]
            cls.QUADROS["ponta_baixo"] = [pygame.transform.rotate(quadro, 270) for quadro in quadros_ponta]

        return cls.QUADROS
    def __checar_lifetime(self, dt, fase):     
        self.__lifetime -= dt
        if (self.__lifetime <= 0):
            fase.remover_entidade(self)
        
    def atualizar(self, dt, fase):
        if (not self.__celulas):
            origem_coluna, origem_linha = Colisor.obter_celula_grid(self.x, self.y)
            self.__celulas.append((origem_coluna, origem_linha, "centro", -1))
            
            # Set de entidades que foram pego no raio da explosão...
            entidades = set(fase.obter_entidades(origem_coluna, origem_linha))
            for direcao in range(4): # 0 = esquerda, 1 = cima, 2 = direita, 3 = baixo
                for i in range(1, self.__raio + 1):
                    coluna, linha = self.__calcular_direcao(origem_coluna, origem_linha, direcao, i)
                    entidades.update(fase.obter_entidades(coluna, linha))
                    if (Colisor.eh_parede(coluna, linha)):
                        # Corrige o anterior para ponta se não for o centro
                        if (i > 1):
                            self.__celulas[-1] = (self.__celulas[-1][0], self.__celulas[-1][1], "ponta", self.__celulas[-1][3]) 
                        break
                
                    tipo = "lado"
                    if i == self.__raio:
                        tipo = "ponta"
                    self.__celulas.append((coluna, linha, tipo, direcao))

            for entidade in entidades:
                if hasattr(entidade, "receber_dano"):
                    entidade.receber_dano(1)
                
        for celula in self.__celulas:
            coluna, linha, tipo, direcao = celula
            animacao = self.__animacoes[(tipo, direcao)]
            animacao.atualizar(dt)
        
        self.__checar_lifetime(dt, fase)
    
    def __calcular_direcao(self, coluna, linha, direcao, i):
        if direcao == 0:  # esquerda
            return coluna - i, linha
        elif direcao == 1:  # cima
            return coluna, linha - i
        elif direcao == 2:  # direita
            return coluna + i, linha
        elif direcao == 3:  # baixo
            return coluna, linha + i

    def desenhar(self, tela):
        for celula in self.__celulas:
            coluna, linha, tipo, direcao = celula
            animacao = self.__animacoes[(tipo, direcao)]
            quadro = animacao.quadro_atual
            x, y = Colisor.centro_da_celula(coluna, linha)
            posicao = quadro.get_rect(center=(x, y))
            tela.blit(quadro, posicao)


