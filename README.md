# BOMB ROYALE

Bomb Royale é uma adaptação de Bomberman desenvolvida sob o paradigma orientado a objetos em Python com
Pygame. Em vez de labirintos contra monstros estáticos, a partida ocorre em formato Battle Royale: o jogador enfrenta 4
bots autônomos que disputam o controle da arena com regras e objetivos idênticos aos do jogador humano (destruir
blocos, coletar itens e eliminar rivais). O último combatente vivo vence a partida.

## Como executar

Requisitos: Python 3 (testado com 3.13).

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

No Windows, use `.venv\Scripts\pip` e `.venv\Scripts\python` no lugar de `.venv/bin/pip` e `.venv/bin/python`.

O ponto de entrada do jogo é o arquivo `main.py`.

## Controles

| Tecla | Ação |
|---|---|
| `W` / `A` / `S` / `D` ou setas | Mover o jogador |
| `ESC` | Sair do jogo |

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `main.py` | Ponto de entrada |
| `bomb_royale/` | Código-fonte (classes do jogo) |
| `assets/` | Imagens e sprite sheets |
| `docs/` | Proposta do jogo e diagrama de classes |
