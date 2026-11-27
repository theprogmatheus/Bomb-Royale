from .arma import Arma


class ArmaCanhao(Arma):
    COOLDOWN = 0.5
    MUNICAO_INICIAL = 1
    TEMPO_DESCARTE = 70.0

    def __init__(self):
        super().__init__(self.COOLDOWN, self.MUNICAO_INICIAL)
        self._tempo_restante = self.TEMPO_DESCARTE

    @property
    def tempo_restante(self):
        return self._tempo_restante

    @property
    def expirada(self):
        return self.municao == 0 or self.tempo_restante == 0

    def atualizar(self, dt):
        super().atualizar(dt)
        self._tempo_restante = max(0.0, self._tempo_restante - dt)

    def disparar(self, combatente, fase):
        if not self.pronta:
            return
        self.municao -= 1
        self._tempo_recarga = self.cooldown
        print("Disparou Canhão")