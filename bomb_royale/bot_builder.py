from .inimigo_bot import InimigoBot


class BotBuilder(InimigoBot):
    def __init__(self, x, y):
        super().__init__("BotBuilder", x, y)

    def tomar_decisao(self):
        self.escolher_direcao_aleatoria()

    def usar_habilidade(self):
        pass

