from abc import ABC, abstractmethod


class Arma(ABC):
    def __init__(self, cooldown, municao=None):
        self._cooldown = cooldown
        self._tempo_recarga = 0.0
        self._municao = None
        self.municao = municao

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def municao(self):
        return self._municao

    @municao.setter
    def municao(self, valor):
        if valor is not None and valor < 0:
            raise ValueError("Munição não pode ser negativa.")
        self._municao = valor

    @property
    def pronta(self):
        tem_municao = self._municao is None or self._municao > 0
        return self._tempo_recarga <= 0 and tem_municao

    def atualizar(self, dt):
        if self._tempo_recarga > 0:
            self._tempo_recarga = max(0.0, self._tempo_recarga - dt)

    @abstractmethod
    def disparar(self, combatente, fase):
        pass
