from .entidade import Entidade
from .colisor import Colisor
from .spritesheet import SpriteSheet
from .animacao import Animacao
from .configuracoes import SPRITE_ENTITY_BOMB


class Bomba(Entidade):
    
    LARGURA = 36
    ALTURA = 36
    
    def __init__(self, arma, combatente, fase, x, y, delay):
        super().__init__(x, y, self.LARGURA, self.ALTURA)
        self.__arma = arma
        self.__combatente = combatente
        self.__fase = fase
        self.__delay = delay
        self.__spritesheet = SpriteSheet(SPRITE_ENTITY_BOMB, 1, 6)
        self.__animacoes = {
            "normal": Animacao(self.__spritesheet.obter_linha(0)[:3]),
            "boom": Animacao(self.__spritesheet.obter_linha(0)[3:])
        }       


    def atualizar(self, dt, fase):
        self.__delay -= dt
        self.__animacoes["normal"].atualizar(dt)
        
        if (self.__delay <= 0):
            # Explode a bomba
            pass

    def desenhar(self, tela):
        quadro = self.__animacoes["normal"].quadro_atual
        posicao = quadro.get_rect(midbottom=self.retangulo.midbottom)
        tela.blit(quadro, posicao)
        
        
        
        
        
        