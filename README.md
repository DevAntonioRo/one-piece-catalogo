# Grand Line Archives ☠️

Wiki interativa inspirada no universo de **One Piece**, integrada ao minigame tático **Grand Line Tower**. Informações sobre personagens, Akuma no Mi, Haki, fraquezas e atributos alimentam diretamente um motor de combate desenvolvido em Python.

> Projeto educacional de fã, sem finalidade comercial. Atributos numéricos e balanceamento do RPG não são dados oficiais.

## O que já funciona

### Wiki

- 12 arquivos de personagens
- Busca por nome ou alcunha
- Filtro e página de tripulações
- Akuma no Mi, tipo, Haki, origem e recompensa
- API JSON em `/api/personagens`

### Grand Line Tower

- Formação de equipe com exatamente três personagens
- Orçamento limitado a 3.200 créditos
- Quatro desafios com dificuldade crescente
- Vida e energia persistentes entre andares
- Recompensas em berries e loja de melhorias
- Recursos táticos limitados: água e Kairouseki
- Diário de combate

### Motor tático

O jogador constrói uma ação escolhendo combatente, aproximação, intensidade, região do alvo, postura, recurso e uso de Haki. O motor considera:

- intangibilidade de Logias;
- Haki do Armamento;
- fraquezas elementais;
- precisão, velocidade, força, técnica e defesa;
- custo de energia;
- postura defensiva ou agressiva;
- atordoamento, enfraquecimento e redução de velocidade;
- decisões reativas dos inimigos.

Exemplo: um ataque físico comum de Zoro causa zero de dano em Crocodile. O mesmo ataque pode atingir o corpo real se estiver imbuído com Haki do Armamento ou se Crocodile tiver sido materializado com água.

## Estrutura

```text
one-piece-catalogo/
├── app.py                 # rotas, sessões e fluxo do jogo
├── data.py                # wiki, atributos e torre
├── game/
│   └── combat.py          # regras e cálculos de combate
├── templates/             # páginas Jinja2
├── static/style.css       # identidade visual responsiva
└── tests/                 # testes da aplicação e do motor
```

## Executando no Windows

Baixe e extraia o ZIP do repositório. Dentro da pasta, clique na barra de endereço do Explorador, digite `cmd` e pressione Enter. Depois execute:

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`.

## Testes

```cmd
python -m unittest discover -s tests -v
```

## Tecnologias

- Python 3
- Flask e Jinja2
- Sessões HTTP
- HTML5 e CSS3
- unittest
