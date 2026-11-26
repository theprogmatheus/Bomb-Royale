from .entidade import Entidade
from .configuracoes import (
    SPRITE_ENTITY_EXPLOSION,
    TAMANHO_CELULA
)
from .spritesheet import SpriteSheet
from .colisor import Colisor
from .bloco import Bloco

class Explosao(Entidade):

    LARGURA = 36
    ALTURA = 36
    QUADROS = None

    def __init__(self, bomba, x, y, raio):
        super().__init__(x, y, self.LARGURA, self.ALTURA)
        self.__bomba = bomba
        self.__raio = raio
        self.__fase = None
    
    @classmethod
    def carregar_quadros(cls):
        if (cls.QUADROS is None):
            cls.QUADROS = []
            sprite_sheet = SpriteSheet(SPRITE_ENTITY_EXPLOSION, 3, 4)
            cls.QUADROS.append(sprite_sheet.obter_linha(0))
            cls.QUADROS.append(sprite_sheet.obter_linha(1))
            cls.QUADROS.append(sprite_sheet.obter_linha(2))
        return cls.QUADROS
    
    def __carregar_animacao(self):
        # Coluna Par e Linha Par: Lugar para colocar bomba
        
        
        pass
    
    def atualizar(self, dt, fase):
        if (self.__fase is None):
            self.__fase = fase

    def desenhar(self, tela):
        # Exigir fase para trabalhar
        if (self.__fase is None):
            return

        coluna, linha = Colisor.obter_celula_grid(self.x, self.y)

        lados = {
            (coluna-1, linha): None,
            (coluna+1, linha): None,
            (coluna, linha+1): None,
            (coluna, linha-1): None
        }

        for entidade in self.__fase.entidades:
            if (isinstance(entidade, Bloco) and not entidade.destrutivel):
                coluna_e, linha_e = Colisor.obter_celula_grid(entidade.x, entidade.y)
                if (coluna_e, linha_e) in lados:
                    lados[(coluna_e, linha_e)] = entidade
                    
                            

        # Continuar a partir daqui...



