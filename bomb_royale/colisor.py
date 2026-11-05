from .configuracoes import TAMANHO_CELULA


class Colisor:
    @staticmethod
    def verificar(a, b):
        return a.retangulo.colliderect(b.retangulo)

    @staticmethod
    def obter_celula_grid(x, y):
        return int(x // TAMANHO_CELULA), int(y // TAMANHO_CELULA)

