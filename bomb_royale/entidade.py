from abc import ABC, abstractmethod

import pygame


class Entidade(ABC):
    def __init__(self, x, y, largura, altura):
        self._x = x
        self._y = y
        self._largura = largura
        self._altura = altura
        self._ativo = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, valor):
        self._x = valor

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, valor):
        self._y = valor

    @property
    def largura(self):
        return self._largura

    @property
    def altura(self):
        return self._altura

    @property
    def ativo(self):
        return self._ativo

    @property
    def retangulo(self):
        return pygame.Rect(int(self._x), int(self._y), self._largura, self._altura)

    def desativar(self):
        self._ativo = False

    @abstractmethod
    def atualizar(self, dt, fase):
        pass

    @abstractmethod
    def desenhar(self, tela):
        pass

