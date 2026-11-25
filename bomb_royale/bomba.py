from .entidade import Entidade
from .colisor import Colisor
from .spritesheet import SpriteSheet
from .animacao import Animacao
from .configuracoes import SPRITE_ENTITY_BOMB


class Bomba(Entidade):
    
    LARGURA = 36
    ALTURA = 36
    
    QUADROS = None
    
    def __init__(self, arma, combatente, fase, x, y, delay):
        super().__init__(x, y, self.LARGURA, self.ALTURA)
        self.__arma = arma
        self.__combatente = combatente
        self.__fase = fase
        self.__delay = delay
        self.__animacoes = {
            "normal": Animacao(self.carregar_quadros()[:3], 0.15),
            "boom": Animacao(self.carregar_quadros()[3:], 0.15)
        }
        
    @classmethod
    def carregar_quadros(cls):
        if (cls.QUADROS is None):
            cls.QUADROS = SpriteSheet(SPRITE_ENTITY_BOMB, 1, 6).obter_linha(0)
        return cls.QUADROS
   
    @property
    def celula(self):
        return Colisor.obter_celula_grid(*self.retangulo.center)
    
    def _explodir(self, fase):
        self.__arma.municao += 1
        
    def _get_tipo(self):
        tipo = "normal"
        if (self.__delay <= 1.1):
            tipo = "boom"
        return tipo

    def atualizar(self, dt, fase):
        self.__delay -= dt
        
        self.__animacoes[self._get_tipo()].atualizar(dt)
        
        if (self.__delay <= 0):
            fase.remover_entidade(self)
            self._explodir(fase)

    def desenhar(self, tela):
        quadro = self.__animacoes[self._get_tipo()].quadro_atual
        posicao = quadro.get_rect(midbottom=self.retangulo.midbottom)
        tela.blit(quadro, posicao)
        
        
        
        
        
        