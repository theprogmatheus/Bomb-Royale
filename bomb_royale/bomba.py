from .entidade import Entidade
from .colisor import Colisor
from .spritesheet import SpriteSheet
from .animacao import Animacao
from .configuracoes import SPRITE_ENTITY_BOMB


class Bomba(Entidade):
    
    LARGURA = 36
    ALTURA = 36
    
    def __init__(self, arma, combatente, fase, x, y, delay):
        
        coluna, linha = Colisor.obter_celula_grid(x,y)
        novoX, novoY = fase.posicao_na_celula(coluna, linha, self.LARGURA, self.ALTURA)
        
        super().__init__(novoX, novoY, self.LARGURA, self.ALTURA)
        self.__arma = arma
        self.__combatente = combatente
        self.__fase = fase
        self.__delay = delay
        self.__spritesheet = SpriteSheet(SPRITE_ENTITY_BOMB, 1, 6)
        self.__animacoes = {
            "normal": Animacao(self.__spritesheet.obter_linha(0)[:3], 0.15),
            "boom": Animacao(self.__spritesheet.obter_linha(0)[3:], 0.15)
        } 
    
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
        
        
        
        
        
        