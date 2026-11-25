from .arma import Arma
from .bomba import Bomba

class ArmaBomba(Arma):
    
    def __init__(self, raio):
        self.__raio = None
        self.raio = raio
        
        super().__init__(cooldown=0, municao=1)
    
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
        
        self.municao -= 1
        
        x = combatente.x
        y = combatente.y        
        bomba = Bomba(self, combatente, fase, x, y, 3)
        fase.adicionar_entidade(bomba)