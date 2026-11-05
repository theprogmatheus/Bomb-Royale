from .configuracoes import SPRITE_BOT_BUILDER
from .inimigo_bot import InimigoBot


class BotBuilder(InimigoBot):
    def __init__(self, x, y):
        super().__init__("BotBuilder", x, y, SPRITE_BOT_BUILDER)

    def tomar_decisao(self):
        self.escolher_direcao_aleatoria()

    def usar_habilidade(self):
        pass
