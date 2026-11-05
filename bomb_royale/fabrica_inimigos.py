from .bot_builder import BotBuilder


class FabricaInimigos:
    TIPOS = {
        "builder": BotBuilder,
    }

    @staticmethod
    def criar(tipo, x, y):
        if tipo not in FabricaInimigos.TIPOS:
            raise ValueError(f"Tipo de inimigo desconhecido: {tipo}")
        return FabricaInimigos.TIPOS[tipo](x, y)

