from .inimigo_bot import InimigoBot
from .configuracoes import SPRITE_BOT_KICKER

class BotKicker(InimigoBot):
    def __init__(self, x, y):
        super().__init__("BotKicker", x,y, SPRITE_BOT_KICKER)

    def tomar_decisao(self, fase):
        self.escolher_direcao_aleatoria()

    def usar_habilidade(self, fase):
        pass 