from .entidade import Entidade
from .configuracoes import SPRITE_ENTITY_EXPLOSION
from .spritesheet import SpriteSheet

class Explosao(Entidade):
    
    QUADROS = None
    
    @classmethod
    def carregar_quadros(cls):
        if (cls.QUADROS is None):
            cls.QUADROS = []
            sprite_sheet = SpriteSheet(SPRITE_ENTITY_EXPLOSION, 3, 4)
            cls.QUADROS.append(sprite_sheet.obter_linha(0))
            cls.QUADROS.append(sprite_sheet.obter_linha(1))
            cls.QUADROS.append(sprite_sheet.obter_linha(2))
            
            
        return cls.QUADROS

    def atualizar(self, dt, fase):
        pass

    def desenhar(self, tela):
        pass