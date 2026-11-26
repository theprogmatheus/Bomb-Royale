from .spritesheet import SpriteSheet

class SpritesheetExplosao(SpriteSheet):
    
    def _calcular_posicao(self, recorte, quadro):
        return recorte.get_rect(center=quadro.get_rect().center)