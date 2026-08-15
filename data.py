"""Conteúdo da wiki e dados balanceados do minigame.

Os campos em ``game`` são valores criados para o RPG e não representam números
oficiais da obra.
"""

CHARACTERS = [
    {
        "slug": "monkey-d-luffy", "name": "Monkey D. Luffy", "epithet": "Chapéu de Palha",
        "crew": "Piratas do Chapéu de Palha", "role": "Capitão", "bounty": 3_000_000_000,
        "origin": "East Blue", "symbol": "☀️", "fruit": "Hito Hito no Mi, Modelo: Nika",
        "fruit_type": "zoan", "haki": ["armament", "observation", "conqueror"],
        "description": "Capitão que navega em busca do One Piece e da liberdade absoluta dos mares.",
        "game": {"cost": 1450, "hp": 1250, "energy": 820, "strength": 92, "defense": 83, "speed": 88, "technique": 86, "haki_level": 3, "element": "rubber"},
    },
    {
        "slug": "roronoa-zoro", "name": "Roronoa Zoro", "epithet": "Caçador de Piratas",
        "crew": "Piratas do Chapéu de Palha", "role": "Espadachim", "bounty": 1_111_000_000,
        "origin": "East Blue", "symbol": "⚔️", "fruit": None, "fruit_type": None,
        "haki": ["armament", "observation", "conqueror"],
        "description": "Espadachim do estilo de três espadas que pretende alcançar o topo do mundo.",
        "game": {"cost": 1200, "hp": 1050, "energy": 720, "strength": 95, "defense": 78, "speed": 74, "technique": 92, "haki_level": 3, "element": "cutting"},
    },
    {
        "slug": "nami", "name": "Nami", "epithet": "Gata Ladra",
        "crew": "Piratas do Chapéu de Palha", "role": "Navegadora", "bounty": 366_000_000,
        "origin": "East Blue", "symbol": "⛈️", "fruit": None, "fruit_type": None, "haki": [],
        "description": "Navegadora brilhante que transforma clima, terreno e informação em vantagem.",
        "game": {"cost": 650, "hp": 650, "energy": 900, "strength": 43, "defense": 48, "speed": 76, "technique": 94, "haki_level": 0, "element": "water"},
    },
    {
        "slug": "sanji", "name": "Sanji", "epithet": "Perna Negra",
        "crew": "Piratas do Chapéu de Palha", "role": "Cozinheiro", "bounty": 1_032_000_000,
        "origin": "North Blue", "symbol": "🔥", "fruit": None, "fruit_type": None,
        "haki": ["armament", "observation"],
        "description": "Cozinheiro e lutador extremamente veloz que procura o lendário All Blue.",
        "game": {"cost": 1050, "hp": 940, "energy": 850, "strength": 87, "defense": 72, "speed": 96, "technique": 89, "haki_level": 2, "element": "fire"},
    },
    {
        "slug": "nico-robin", "name": "Nico Robin", "epithet": "Criança Demônio",
        "crew": "Piratas do Chapéu de Palha", "role": "Arqueóloga", "bounty": 930_000_000,
        "origin": "West Blue", "symbol": "📜", "fruit": "Hana Hana no Mi", "fruit_type": "paramecia",
        "haki": [], "description": "A única sobrevivente de Ohara capaz de ler os Poneglyphs.",
        "game": {"cost": 800, "hp": 720, "energy": 860, "strength": 68, "defense": 55, "speed": 67, "technique": 95, "haki_level": 0, "element": "control"},
    },
    {
        "slug": "brook", "name": "Brook", "epithet": "Soul King",
        "crew": "Piratas do Chapéu de Palha", "role": "Músico", "bounty": 383_000_000,
        "origin": "West Blue", "symbol": "🎻", "fruit": "Yomi Yomi no Mi", "fruit_type": "paramecia",
        "haki": [], "description": "Músico esqueleto que deseja cumprir a promessa de sua tripulação a Laboon.",
        "game": {"cost": 700, "hp": 690, "energy": 920, "strength": 59, "defense": 50, "speed": 98, "technique": 84, "haki_level": 0, "element": "ice"},
    },
    {
        "slug": "jinbe", "name": "Jinbe", "epithet": "Cavaleiro do Mar",
        "crew": "Piratas do Chapéu de Palha", "role": "Timoneiro", "bounty": 1_100_000_000,
        "origin": "Ilha dos Homens-Peixe", "symbol": "🌊", "fruit": None, "fruit_type": None,
        "haki": ["armament", "observation"], "description": "Mestre do karatê dos homens-peixe e experiente combatente dos mares.",
        "game": {"cost": 1100, "hp": 1180, "energy": 760, "strength": 86, "defense": 92, "speed": 65, "technique": 88, "haki_level": 2, "element": "water"},
    },
    {
        "slug": "trafalgar-law", "name": "Trafalgar D. Water Law", "epithet": "Cirurgião da Morte",
        "crew": "Piratas Heart", "role": "Capitão e médico", "bounty": 3_000_000_000,
        "origin": "North Blue", "symbol": "🫀", "fruit": "Ope Ope no Mi", "fruit_type": "paramecia",
        "haki": ["armament", "observation"], "description": "Médico estrategista que manipula tudo dentro de seu campo de operação.",
        "game": {"cost": 1400, "hp": 880, "energy": 1050, "strength": 76, "defense": 66, "speed": 83, "technique": 99, "haki_level": 2, "element": "spatial"},
    },
    {
        "slug": "crocodile", "name": "Crocodile", "epithet": "Rei do Deserto",
        "crew": "Cross Guild", "role": "Oficial-chefe", "bounty": 1_965_000_000,
        "origin": "Grand Line", "symbol": "🏜️", "fruit": "Suna Suna no Mi", "fruit_type": "logia",
        "haki": [], "description": "Pirata calculista capaz de controlar areia e retirar a umidade de seus alvos.",
        "weaknesses": ["water", "seastone"],
        "game": {"cost": 1300, "hp": 1150, "energy": 900, "strength": 82, "defense": 79, "speed": 76, "technique": 94, "haki_level": 0, "element": "sand"},
    },
    {
        "slug": "enel", "name": "Enel", "epithet": "Deus de Skypiea",
        "crew": "Forças de Enel", "role": "Governante", "bounty": 0,
        "origin": "Ilha do Céu Birka", "symbol": "⚡", "fruit": "Goro Goro no Mi", "fruit_type": "logia",
        "haki": ["observation"], "description": "Usuário de uma Logia elétrica com percepção ampliada por seu Mantra.",
        "weaknesses": ["rubber", "seastone"],
        "game": {"cost": 1350, "hp": 1080, "energy": 1050, "strength": 79, "defense": 70, "speed": 96, "technique": 96, "haki_level": 2, "element": "lightning"},
    },
    {
        "slug": "rob-lucci", "name": "Rob Lucci", "epithet": "Arma de Massacre",
        "crew": "CP0", "role": "Agente", "bounty": 0,
        "origin": "Grand Line", "symbol": "🐆", "fruit": "Neko Neko no Mi, Modelo: Leopardo", "fruit_type": "zoan",
        "haki": ["armament", "observation"], "description": "Agente especialista em Rokushiki e combate corpo a corpo.",
        "game": {"cost": 1250, "hp": 1280, "energy": 820, "strength": 90, "defense": 88, "speed": 91, "technique": 90, "haki_level": 2, "element": "physical"},
    },
    {
        "slug": "kaido", "name": "Kaido", "epithet": "Rei das Feras",
        "crew": "Piratas das Feras", "role": "Capitão", "bounty": 4_611_100_000,
        "origin": "Grand Line", "symbol": "🐉", "fruit": "Uo Uo no Mi, Modelo: Seiryu", "fruit_type": "mythical_zoan",
        "haki": ["armament", "observation", "conqueror"], "description": "Combatente de resistência absurda capaz de assumir a forma de um dragão lendário.",
        "game": {"cost": 2000, "hp": 1750, "energy": 980, "strength": 99, "defense": 99, "speed": 82, "technique": 91, "haki_level": 3, "element": "dragon"},
    },
]

CREWS = [
    {"name": "Piratas do Chapéu de Palha", "captain": "Monkey D. Luffy", "ship": "Thousand Sunny", "symbol": "☀️", "description": "Uma pequena tripulação unida por sonhos enormes e pela busca da liberdade."},
    {"name": "Piratas Heart", "captain": "Trafalgar D. Water Law", "ship": "Polar Tang", "symbol": "♥️", "description": "Tripulação médica e estratégica originária do North Blue."},
    {"name": "Cross Guild", "captain": "Buggy", "ship": "Big Top Blaster", "symbol": "🎪", "description": "Organização que oferece recompensas por membros da Marinha."},
    {"name": "CP0", "captain": "Governo Mundial", "ship": "Confidencial", "symbol": "♟️", "description": "Agência de inteligência de elite ligada aos Nobres Mundiais."},
    {"name": "Piratas das Feras", "captain": "Kaido", "ship": "Hassaikai", "symbol": "🐉", "description": "Tripulação construída em torno de poder, Zoans e hierarquia militar."},
]

TOWER = [
    {"enemy": "rob-lucci", "name": "Portão da Justiça", "reward": 1800, "hint": "Um adversário veloz e resistente. Controle sua energia."},
    {"enemy": "crocodile", "name": "Tempestade de Areia", "reward": 2600, "hint": "Ataques comuns atravessam uma Logia. Haki ou água podem mudar a luta."},
    {"enemy": "enel", "name": "Julgamento do Céu", "reward": 3400, "hint": "Eletricidade, velocidade e intangibilidade tornam este combate imprevisível."},
    {"enemy": "kaido", "name": "O Teto do Mundo", "reward": 6000, "hint": "Somente uma equipe aprimorada sobreviverá ao último andar."},
]


def get_character(slug):
    return next((character for character in CHARACTERS if character["slug"] == slug), None)


def crew_members(crew_name):
    return [character for character in CHARACTERS if character["crew"] == crew_name]
