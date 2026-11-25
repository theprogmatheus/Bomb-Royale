from .bot_builder import BotBuilder
from .bot_kicker import BotKicker


class FabricaInimigos:
    TIPOS = {
        "builder": BotBuilder,
        "kicker": BotKicker,
    }

    @staticmethod
    def criar(tipo, x, y):
        if tipo not in FabricaInimigos.TIPOS:
            raise ValueError(f"Tipo de inimigo desconhecido: {tipo}")
        return FabricaInimigos.TIPOS[tipo](x, y)

