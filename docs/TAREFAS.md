## Divisão de Tarefas por Integrante

### Matheus — Sistema de Armas, Bombas, Explosões e Arena
- **Branch:** `feat/armas-combate`
- **Arquivos NOVOS:** `bomb_royale/arma_bomba.py`, `bomb_royale/bomba.py`, `bomb_royale/explosao.py`
- **Arquivos EXISTENTES (só Matheus edita):** `combatente.py`, `fase.py`, `jogador.py`, `bot_builder.py`
- **Requisitos de POO cobertos:** Composição (`Combatente` contém `Arma`), Polimorfismo (`Bomba` e `Explosao` herdando de `Entidade` e rodando no mesmo laço da `Fase`).
- **Checklist Etapa 3 (até 26/11):**
  - [ ] Subir o **Passo 0 (Contrato)** na `main` e adicionar os 3 colegas como Collaborators.
  - [ ] Criar `Bomba(Entidade)` (timer até explodir, desenha bomba na tela) e `Explosao(Entidade)` (timer curto, desenha explosão em cruz).
  - [ ] Criar `ArmaBomba(Arma)` que instancia `Bomba` na posição do combatente e adiciona na `fase`.
  - [ ] Adicionar composição `self._arma` (com `@property` e setter) e atributo `_pontuacao` no `Combatente`.
  - [ ] Conectar tecla `Espaço` no `Jogador` para disparar arma e tecla `E` para `usar_habilidade(fase)`.
  - [ ] Gerar blocos destrutíveis (`Bloco(x, y, destrutivel=True)`) aleatoriamente na `Fase` (mantendo cantos de spawn livres).
- **Checklist Mostra Final (até 02/12):**
  - [ ] Explosão destrói blocos destrutíveis, aplica dano em combatentes e soma pontos para o autor da bomba.
  - [ ] Implementar habilidade do `BotBuilder` (posicionar até 5 blocos destrutíveis com delay de 3s).
  - [ ] IA básica em `InimigoBot` para soltar bombas e tentar desviar da zona de explosão.

---

### Gabriel — Placar, Ranking, Encapsulamento, HUD e Fluxo de Partida
- **Branch:** `feat/placar-hud`
- **Arquivos NOVOS:** `bomb_royale/placar.py`, `bomb_royale/hud.py`
- **Arquivos EXISTENTES (só Gabriel edita):** `jogo.py` (e revisão final dos setters `@property` em `combatente.py` após o merge do Matheus)
- **Requisitos de POO cobertos:** Métodos especiais (`__str__`, `__lt__`, `__eq__`), Composição (`Jogo` contém `Jogador`, `Fase` e `Placar`), Encapsulamento com validação (`@property` + setters de `vida`, `municao` e `pontuacao`).
- **Checklist Etapa 3 (até 26/11):**
  - [ ] Criar `RegistroRanking` em `placar.py` com `nome` e `pontos`, implementando `__lt__`, `__eq__` e `__str__` (permitindo `sorted()` direto).
  - [ ] Criar classe `Placar` em `placar.py` (armazena registros, registra pontuação por combatente, retorna ranking ordenado).
  - [ ] Compor `self._placar = Placar()` na classe `Jogo` (com `@property placar`).
  - [ ] Garantir validação estrita nos setters de `vida`, `pontuacao` (em `Combatente`) e `municao` (em `Arma`) — impedindo valores negativos.
  - [ ] Criar `HUD` básico em `hud.py` mostrando na tela: vida do jogador, pontuação e arma atual.
- **Checklist Mostra Final (até 02/12):**
  - [ ] Implementar detecção de fim de partida no `Jogo` (último combatente vivo vence ou jogador morre).
  - [ ] Criar tela de Vitória / Game Over exibindo o ranking ordenado usando `str(registro)` e opção de reiniciar (`R`) ou sair (`ESC`).
  - [ ] Mostrar cooldown da habilidade e timer do Canhão Direcional (70s) no HUD.

---

### Gustavo — Hierarquia de Inimigos (Parte 1) e Fábrica (`@classmethod`)
- **Branch:** `feat/bots-kicker-jumper`
- **Arquivos NOVOS:** `bomb_royale/bot_kicker.py`, `bomb_royale/bot_jumper.py`
- **Arquivos EXISTENTES (só Gustavo edita):** `fabrica_inimigos.py`
- **Requisitos de POO cobertos:** Herança (subclasses de `InimigoBot`), `@classmethod` (`FabricaInimigos.criar()`), Polimorfismo.
- **Checklist Etapa 3 (até 26/11):**
  - [ ] Criar `BotKicker(InimigoBot)` usando `SPRITE_BOT_KICKER`, implementando `tomar_decisao(fase)` e `usar_habilidade(fase)` (estrutura inicial + cooldown de 60s).
  - [ ] Criar `BotJumper(InimigoBot)` usando `SPRITE_BOT_JUMPER`, implementando `tomar_decisao(fase)` e `usar_habilidade(fase)` (estrutura inicial + cooldown de 15s).
  - [ ] Atualizar `FabricaInimigos.criar(cls, tipo, x, y)` para usar **`@classmethod`** (em vez de `@staticmethod`), usando `cls.TIPOS` e registrando `"builder"`, `"kicker"` e `"jumper"`.
  - [ ] Garantir que `Jogo` consiga instanciar os diferentes bots via `FabricaInimigos.criar(...)` nos cantos da arena.
- **Checklist Mostra Final (até 02/12):**
  - [ ] Habilidade real do `BotKicker`: detectar bomba adjacente e fazê-la deslizar em linha reta pelo grid até colidir com obstáculo sólido.
  - [ ] Habilidade real do `BotJumper`: pular exatamente 1 bloco sólido adjacente na direção do movimento (bloqueando se houver 2 blocos seguidos).

---

### Lucas — Hierarquia de Inimigos (Parte 2) e Canhão Direcional (Pickup)
- **Branch:** `feat/bots-smoker-angel-canhao`
- **Arquivos NOVOS:** `bomb_royale/bot_smoker.py`, `bomb_royale/bot_angel.py`, `bomb_royale/arma_canhao.py`, `bomb_royale/canhao_pickup.py`
- **Arquivos EXISTENTES:** após o merge do Gustavo, adiciona 2 linhas em `fabrica_inimigos.py` (`"smoker"` e `"angel"`) e adiciona spawn de `CanhaoPickup` na `Fase`.
- **Requisitos de POO cobertos:** Herança (completa as 5 especializações da proposta), Troca dinâmica de composição (`ArmaBomba` ↔ `ArmaCanhao`), Entidade coletável polimórfica.
- **Checklist Etapa 3 (até 26/11):**
  - [ ] Criar `BotSmoker(InimigoBot)` usando `SPRITE_BOT_SMOKER` (estrutura inicial + cooldown de 60s).
  - [ ] Criar `BotAngel(InimigoBot)` usando `SPRITE_BOT_ANGEL` (estrutura inicial + lógica condicional: vida extra quando >2 vivos, boost no 1x1).
  - [ ] Criar `ArmaCanhao(Arma)` herdando de `Arma`, com munição `1` e temporizador de descarte de **70 segundos**.
  - [ ] Criar `CanhaoPickup(Entidade)` coletável na arena (desenha item no mapa e detecta coleta usando `Colisor.verificar`).
- **Checklist Mostra Final (até 02/12):**
  - [ ] Disparo linear instantâneo da `ArmaCanhao` (percorre linha reta até o primeiro obstáculo, detonando bombas, destruindo blocos e eliminando combatentes).
  - [ ] Respawn automático do `CanhaoPickup` em célula livre aleatória após o disparo ou após o timeout de 70s.
  - [ ] Habilidade real do `BotSmoker` (entidade de cortina de fumaça que oculta bombas/jogadores por alguns segundos) e `BotAngel` (1 vida extra ou boost de velocidade de 5s no 1x1).

---