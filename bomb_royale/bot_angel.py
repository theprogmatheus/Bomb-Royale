from .combatente import Combatente
from .configuracoes import SPRITE_BOT_ANGEL
from .inimigo_bot import InimigoBot


class BotAngel(InimigoBot):
    COOLDOWN_HABILIDADE = 30.0
    DURACAO_BOOST = 5.0
    MULTIPLICADOR_BOOST = 1.5

    def __init__(self, x, y):
        super().__init__("BotAngel", x, y, SPRITE_BOT_ANGEL)
        # O tempo de recarga começa em 15, e não em 0 como o normal,
        # para que ele não se cure logo que a partida começa,
        # e não usa a mesma constante de cooldown para que seja um
        # intervalo menor
        self._tempo_recarga_habilidade = 15.0
        self._vida_extra_usada = False
        self._tempo_boost_velocidade = 0.0

    @property
    def habilidade_pronta(self):
        return self._tempo_recarga_habilidade <= 0

    def _contar_vivos(self, fase):
        vivos = [e for e in fase.entidades if isinstance(e, Combatente) and e.ativo]
        return len(vivos)

    def tomar_decisao(self, fase):
        self.escolher_direcao_aleatoria()
        self.usar_habilidade(fase)

    def usar_habilidade(self, fase):
        if not self.habilidade_pronta:
            return
        criaturas = self._contar_vivos(fase)
        if criaturas > 2 and not self._vida_extra_usada:
            self._vida += 1
            self._vida_extra_usada = True
        elif criaturas == 2:
            self._tempo_boost_velocidade = self.DURACAO_BOOST
            # cooldown só ativa dentro do boost de velocidade porque
            # a vida extra já tem limite (uma vez) e se ele se curar 
            # e logo depois começar o 1v1, ele já deve ter o boost de
            # velocidade desde o início
            self._tempo_recarga_habilidade = self.COOLDOWN_HABILIDADE 

    def mover(self, direcao_x, direcao_y, dt, fase):
        if self._tempo_boost_velocidade == 0:
            return super().mover(direcao_x, direcao_y, dt, fase)
        else:
            return super().mover(direcao_x, direcao_y, dt*self.MULTIPLICADOR_BOOST, fase)

    def atualizar(self, dt, fase):
        super().atualizar(dt, fase)
        self._tempo_boost_velocidade = max(0.0, self._tempo_boost_velocidade - dt)
        self._tempo_recarga_habilidade = max(0.0, self._tempo_recarga_habilidade - dt)
