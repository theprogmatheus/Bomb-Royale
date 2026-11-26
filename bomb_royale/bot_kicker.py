from .inimigo_bot import InimigoBot
from .configuracoes import SPRITE_BOT_KICKER, COOLDOWN_HABILIDADE_KICKER


class BotKicker(InimigoBot):
    def __init__(self, x, y):
        super().__init__("BotKicker", x, y, SPRITE_BOT_KICKER)
        self._tempo_recarga_habilidade = 0.0

    @property
    def habilidade_pronta(self):
        return self._tempo_recarga_habilidade <= 0

    def tomar_decisao(self, fase):
        self.escolher_direcao_aleatoria()
        self.usar_habilidade(fase)

    def usar_habilidade(self, fase):
        if not self.habilidade_pronta:
            return
        print("Kicker usou a habilidade")
        self._tempo_recarga_habilidade = COOLDOWN_HABILIDADE_KICKER

    def atualizar(self, dt, fase):
        super().atualizar(dt, fase)
        self._tempo_recarga_habilidade = max(0.0, self._tempo_recarga_habilidade - dt)
