from .arma import Arma
from .bomba import Bomba
from .colisor import Colisor

class ArmaBomba(Arma):
    
    def __init__(self, raio):
        self.__raio = None
        self.raio = raio
        
        super().__init__(cooldown=0, municao=3)
    
    @property
    def raio(self):
        return self.__raio
        
    @raio.setter
    def raio(self, novo_raio):
        if (novo_raio < 1):
            novo_raio = 1
        self.__raio = novo_raio
    
    def disparar(self, combatente, fase):
        if (self.municao < 1):
            return
        
        # TODO: Verificar se já existe uma bomba posicionada nesse quadrado
        
        proibidoColocarBomba = False
        
        coluna, linha = Colisor.obter_celula_grid(*combatente.retangulo.center)        
        bombas = [entidade for entidade in fase.entidades if isinstance(entidade, Bomba)]
        for bomba in bombas:
            if bomba.celula == (coluna, linha):
                proibidoColocarBomba = True
                break
        
        if (proibidoColocarBomba):
            return
        
        self.municao -= 1
        
        bomba = Bomba(self, combatente, fase, combatente.x, combatente.y, 3)
        fase.adicionar_entidade(bomba)