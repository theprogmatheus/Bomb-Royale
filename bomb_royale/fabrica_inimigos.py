from .bot_builder import BotBuilder
from .bot_kicker import BotKicker
from .bot_jumper import BotJumper
from .bot_angel import BotAngel
from .bot_smoker import BotSmoker


class FabricaInimigos:
    TIPOS = {
        "builder": BotBuilder,
        "kicker": BotKicker,
        "jumper": BotJumper,
        "smoker": BotSmoker,
        "angel": BotAngel
    }

    #Usar classmethod permite que caso uma subclasse de fábrica seja criada com outro dicionario o cls.TIPOS usará o da subclasse.
    
    @classmethod
    def criar(cls, tipo, x, y):
        if tipo not in cls.TIPOS:
            raise ValueError(f"Tipo de inimigo desconhecido: {tipo}")
        return cls.TIPOS[tipo](x, y)

