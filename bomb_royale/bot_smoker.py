from .configuracoes import SPRITE_BOT_SMOKER
from .inimigo_bot import InimigoBot


class BotSmoker(InimigoBot):
    COOLDOWN_HABILIDADE = 60.0

    def __init__(self, x, y):
        super().__init__("BotSmoker", x, y, SPRITE_BOT_SMOKER)
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
        print("Usou a habilidade de fumaça")
        self._tempo_recarga_habilidade = self.COOLDOWN_HABILIDADE

    def atualizar(self, dt, fase):
        super().atualizar(dt, fase)
        self._tempo_recarga_habilidade = max(0.0, self._tempo_recarga_habilidade - dt)
