# Grand Line Archives ☠️

Wiki interativa inspirada no universo de **One Piece**, integrada ao minigame tático **Grand Line Tower**. Informações sobre personagens, Akuma no Mi, Haki, fraquezas e atributos alimentam diretamente um motor de combate desenvolvido em Python.

> Projeto educacional de fã, sem finalidade comercial. Atributos numéricos e balanceamento do RPG não são dados oficiais.

## O que já funciona

### Wiki

- 33 personagens cadastrados
- Busca por nome ou alcunha
- Filtro e página de tripulações
- Akuma no Mi, tipo, Haki, origem e recompensa
- API JSON em `/api/personagens`

### Grand Line Tower

- Formação de equipe com exatamente três personagens e 25 opções recrutáveis
- Orçamento limitado a 4.200 créditos
- Cinco desafios com dificuldade crescente e Barba Negra como chefe final
- Vida e energia persistentes entre andares
- Recompensas em berries e loja de melhorias
- Recursos táticos limitados: água e Kairouseki
- Diário de combate

### Motor tático

O jogador planeja uma ação separada para cada integrante. Todas as ordens entram em uma linha temporal junto com o inimigo e são resolvidas por velocidade. Personagens rápidos acumulam iniciativa e podem agir novamente antes de combatentes lentos. O motor considera:

- intangibilidade de Logias;
- Haki do Armamento;
- fraquezas elementais;
- precisão, velocidade, força, técnica e defesa;
- crítico calculado a partir da técnica;
- ações extras por iniciativa acumulada;
- custo de energia;
- cooldown de habilidades;
- postura defensiva ou agressiva;
- atordoamento, enfraquecimento e redução de velocidade;
- imunidades por tipo de dano, como Buggy contra cortes e Crocodile contra golpes normais sem Haki ou recursos capazes de atingir seu corpo;
- passivas, cura, controle e sinergias de facção.

Exemplos: um ataque comum de Zoro causa zero de dano em Crocodile sem Haki; qualquer corte causa zero de dano em Buggy; ROOM ignora a defesa; Vórtice Sombrio bloqueia habilidades; e Gear 5 fortalece Luffy em situação crítica.

## Próximos passos

O desenvolvimento continuará dividido entre a expansão da wiki, o aprofundamento do RPG e a evolução técnica da aplicação.

### Wiki e universo

- Adicionar novos personagens, tripulações, organizações e ilhas.
- Separar piratas, marinheiros, revolucionários e outras facções.
- Expandir a lore com histórias, relações, habilidades e acontecimentos importantes.
- Criar páginas específicas para Akuma no Mi, tipos de Haki e localizações.
- Adicionar recompensas para marinheiros com base no sistema da Cross Guild.
- Classificar personagens como jogáveis, desbloqueáveis, chefes ou exclusivos da wiki.

### Grand Line Tower

- Adicionar novos ataques, passivas, transformações e despertares.
- Ampliar a variedade de itens e recursos táticos.
- Criar novos andares, chefes e desafios especiais.
- Implementar níveis de dificuldade.
- Melhorar a inteligência e a tomada de decisões dos inimigos.
- Adicionar modos de sobrevivência, treinamento e batalha contra chefes.
- Criar um sistema de desbloqueio e evolução de personagens.
- Permitir estratégias mais detalhadas para cada ação de combate.

### Progressão

- Salvar equipes, berries, habilidades e progresso do jogador.
- Criar perfis de jogador e histórico de partidas.
- Adicionar conquistas e desafios opcionais.
- Implementar uma loja com habilidades, itens e melhorias permanentes.

### Evolução técnica

- Substituir os dados estáticos por um banco de dados relacional.
- Utilizar SQLAlchemy para persistência dos dados.
- Expandir os testes automatizados do motor e das rotas Flask.
- Documentar os endpoints da API.
- Adicionar validação de dados, tratamento de erros e logs.
- Configurar testes automáticos com GitHub Actions.
- Preparar a aplicação para publicação online.

### Interface

- Melhorar a experiência de planejamento das ações.
- Criar indicadores visuais para energia, cooldown e efeitos de status.
- Adicionar animações e feedback visual durante o combate.
- Aprimorar a responsividade para dispositivos móveis.
- Implementar melhorias de acessibilidade.

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
