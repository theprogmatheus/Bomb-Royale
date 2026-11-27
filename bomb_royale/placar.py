class RegistroRanking:
    def __init__(self, nome, pontos=0):
        self._nome = ""
        self._pontos = 0
        self.nome = nome
        self.pontos = pontos

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome do combatente não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def pontos(self):
        return self._pontos

    @pontos.setter
    def pontos(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("Pontuação deve ser um número inteiro.")
        if valor < 0:
            raise ValueError("Pontuação não pode ser negativa.")
        self._pontos = valor

    def adicionar_pontos(self, quantidade):
        if not isinstance(quantidade, int) or isinstance(quantidade, bool):
            raise ValueError("Quantidade de pontos deve ser um número inteiro.")
        if quantidade < 0:
            raise ValueError("Quantidade de pontos não pode ser negativa.")
        self._pontos += quantidade

    def __lt__(self, outro):
        if not isinstance(outro, RegistroRanking):
            return NotImplemented
        return self._pontos < outro._pontos

    def __eq__(self, outro):
        if not isinstance(outro, RegistroRanking):
            return NotImplemented
        return self._nome == outro._nome and self._pontos == outro._pontos

    def __str__(self):
        return f"{self._nome}: {self._pontos} pts"

    def __repr__(self):
        return f"RegistroRanking(nome={self._nome!r}, pontos={self._pontos})"


class Placar:
    def __init__(self):
        self._registros = {}

    @property
    def registros(self):
        return self.obter_ranking()

    def registrar_combatente(self, nome, pontos_iniciais=0):
        if nome not in self._registros:
            self._registros[nome] = RegistroRanking(nome, pontos_iniciais)
        return self._registros[nome]

    def adicionar_pontos(self, nome, quantidade):
        registro = self.registrar_combatente(nome)
        registro.adicionar_pontos(quantidade)

    def definir_pontos(self, nome, pontos):
        registro = self.registrar_combatente(nome)
        registro.pontos = pontos

    def obter_pontos(self, nome):
        registro = self._registros.get(nome)
        return registro.pontos if registro else 0

    def obter_ranking(self):
        return sorted(self._registros.values(), reverse=True)

    def sincronizar_combatente(self, combatente):
        pontos = getattr(combatente, "pontuacao", None)
        if pontos is not None:
            self.definir_pontos(combatente.nome, pontos)
        else:
            self.registrar_combatente(combatente.nome)

    def limpar(self):
        self._registros.clear()

    def __len__(self):
        return len(self._registros)

    def __str__(self):
        linhas = [
            f"{posicao}. {registro}"
            for posicao, registro in enumerate(self.obter_ranking(), start=1)
        ]
        return "\n".join(linhas) if linhas else "Sem registros no placar."
