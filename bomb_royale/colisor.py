from .configuracoes import (
    TAMANHO_CELULA,
    COLUNAS,
    LINHAS
)


class Colisor:
    
    @staticmethod
    def verificar(a, b):
        return a.retangulo.colliderect(b.retangulo)

    @staticmethod
    def obter_celula_grid(x, y):
        return int(x // TAMANHO_CELULA), int(y // TAMANHO_CELULA)
    
    @staticmethod
    def eh_caminho(coluna, linha):
        
        # Se a coluna ou linha estiver fora dos limites, não é caminho
        if (coluna <= 0 or coluna >= COLUNAS-1):
            return False
        
        # Se a linha estiver fora dos limites, não é caminho
        if (linha <= 0 or linha >= LINHAS-1):
            return False
        
        return coluna % 2 != 0 or linha % 2 != 0
    
    @staticmethod
    def eh_parede(coluna, linha):
        return not Colisor.eh_caminho(coluna, linha)

    @staticmethod
    def centro_da_celula(coluna, linha):
        x = coluna * TAMANHO_CELULA + (TAMANHO_CELULA / 2)
        y = linha * TAMANHO_CELULA + (TAMANHO_CELULA / 2)
        return x, y