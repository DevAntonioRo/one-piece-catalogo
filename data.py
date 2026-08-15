"""Wiki e balanceamento do Grand Line Tower.

Os atributos e custos são números não oficiais criados para o minigame.
"""

SKILLS = {
    "basic": {"name": "Ataque básico", "power": 1.0, "energy": 22, "cooldown": 0, "effect": None},
    "conqueror_strike": {"name": "Impacto do Conquistador", "power": 1.55, "energy": 64, "cooldown": 2, "effect": "stun", "haki": True},
    "precision_cut": {"name": "Corte de precisão", "power": 1.42, "energy": 48, "cooldown": 1, "effect": "bleed", "damage_type": "cutting"},
    "ifrit": {"name": "Ifrit Jambe", "power": 1.40, "energy": 46, "cooldown": 1, "effect": "burn", "damage_type": "fire"},
    "water_shock": {"name": "Vagabond Drill", "power": 1.28, "energy": 38, "cooldown": 1, "effect": "soaked", "damage_type": "water"},
    "clutch": {"name": "Clutch", "power": 1.05, "energy": 35, "cooldown": 1, "effect": "restrained", "ignore_defense": .35},
    "radical_beam": {"name": "Radical Beam", "power": 1.55, "energy": 60, "cooldown": 2, "effect": "burn", "damage_type": "energy"},
    "soul_freeze": {"name": "Corte da Alma", "power": 1.18, "energy": 34, "cooldown": 1, "effect": "frozen", "damage_type": "ice"},
    "monster_point": {"name": "Monster Point", "power": 1.50, "energy": 55, "cooldown": 2, "effect": "guard_break"},
    "medical_care": {"name": "Tratamento de Emergência", "power": .10, "energy": 52, "cooldown": 2, "effect": "heal_team"},
    "thunderbolt": {"name": "Thunderbolt Tempo", "power": 1.36, "energy": 45, "cooldown": 1, "effect": "shocked", "damage_type": "lightning"},
    "pop_green": {"name": "Pop Green", "power": .92, "energy": 28, "cooldown": 1, "effect": "restrained", "damage_type": "plant"},
    "divine_departure": {"name": "Kamusari", "power": 1.85, "energy": 78, "cooldown": 2, "effect": "stun", "haki": True},
    "quake": {"name": "Terremoto", "power": 1.82, "energy": 82, "cooldown": 2, "effect": "guard_break", "damage_type": "quake", "area": True},
    "phoenix_flame": {"name": "Chamas da Fênix", "power": 1.05, "energy": 48, "cooldown": 2, "effect": "regenerate"},
    "fire_fist": {"name": "Hiken", "power": 1.48, "energy": 58, "cooldown": 2, "effect": "burn", "damage_type": "fire"},
    "dark_vortex": {"name": "Vórtice Sombrio", "power": 1.30, "energy": 55, "cooldown": 2, "effect": "silenced", "damage_type": "darkness"},
    "ice_age": {"name": "Ice Age", "power": 1.38, "energy": 62, "cooldown": 2, "effect": "frozen", "damage_type": "ice"},
    "world_cut": {"name": "Corte da Yoru", "power": 1.70, "energy": 62, "cooldown": 2, "effect": "bleed", "damage_type": "cutting"},
    "desert": {"name": "Deserto Spada", "power": 1.34, "energy": 48, "cooldown": 1, "effect": "dehydrated", "damage_type": "sand"},
    "buggy_ball": {"name": "Buggy Ball", "power": 1.08, "energy": 35, "cooldown": 1, "effect": "burn", "damage_type": "explosive"},
    "room": {"name": "ROOM: Shock Wille", "power": 1.46, "energy": 74, "cooldown": 2, "effect": "internal_damage", "ignore_defense": 1.0},
    "damned_punk": {"name": "Damned Punk", "power": 1.58, "energy": 68, "cooldown": 2, "effect": "shocked", "damage_type": "magnetic"},
    "galaxy_impact": {"name": "Galaxy Impact", "power": 1.75, "energy": 72, "cooldown": 2, "effect": "stun", "haki": True},
    "honesty": {"name": "Honesty Impact", "power": 1.38, "energy": 50, "cooldown": 2, "effect": "guard_break", "haki": True},
    "dragon_claw": {"name": "Garra de Dragão", "power": 1.42, "energy": 48, "cooldown": 1, "effect": "guard_break", "damage_type": "fire"},
    "dark_king": {"name": "Lâmina do Rei das Trevas", "power": 1.58, "energy": 58, "cooldown": 2, "effect": "stun", "haki": True},
    "divine_glacier": {"name": "Glaciação Divina", "power": 1.48, "energy": 55, "cooldown": 2, "effect": "frozen", "damage_type": "ice"},
    "future_mochi": {"name": "Mochi do Futuro", "power": 1.32, "energy": 44, "cooldown": 1, "effect": "restrained"},
    "perfume_femur": {"name": "Perfume Femur", "power": 1.34, "energy": 45, "cooldown": 1, "effect": "petrified"},
    "parasite": {"name": "Parasite", "power": 1.10, "energy": 52, "cooldown": 2, "effect": "controlled"},
    "togen": {"name": "Togen Totsuka", "power": 1.70, "energy": 65, "cooldown": 2, "effect": "bleed", "damage_type": "cutting", "haki": True},
    "thunder_bagua": {"name": "Raimei Hakke", "power": 1.78, "energy": 70, "cooldown": 2, "effect": "stun", "haki": True},
    "rokuogan": {"name": "Rokuogan", "power": 1.42, "energy": 50, "cooldown": 1, "effect": "internal_damage", "ignore_defense": .55},
    "el_thor": {"name": "El Thor", "power": 1.62, "energy": 66, "cooldown": 2, "effect": "shocked", "damage_type": "lightning"},
}


def _c(slug, name, epithet, crew, role, symbol, stats, *, fruit=None, fruit_type=None,
       haki=(), archetype="DPS", skill="basic", passive=None, playable=True,
       damage_type="physical", bounty=0, origin="Grand Line", description=None,
       weaknesses=(), immunities=()):
    hp, strength, defense, speed, technique = stats
    cost = round((strength + defense + speed + technique) * 2.25 + hp * .28)
    return {
        "slug": slug, "name": name, "epithet": epithet, "crew": crew, "role": role,
        "bounty": bounty, "origin": origin, "symbol": symbol, "fruit": fruit,
        "fruit_type": fruit_type, "haki": list(haki), "archetype": archetype,
        "skill": skill[0] if isinstance(skill, tuple) else skill,
        "skills": list(skill) if isinstance(skill, tuple) else [skill],
        "passive": passive, "playable": playable,
        "damage_type": damage_type, "weaknesses": list(weaknesses),
        "immunities": list(immunities),
        "description": description or f"Arquivo tático de {name}.",
        "game": {"cost": cost, "hp": hp, "energy": 600 + technique * 4,
                 "strength": strength, "defense": defense, "speed": speed,
                 "technique": technique, "haki_level": len(haki)},
    }


CHARACTERS = [
    _c("monkey-d-luffy","Monkey D. Luffy","Chapéu de Palha","Piratas do Chapéu de Palha","Capitão","☀️",(2100,97,94,96,95),fruit="Hito Hito no Mi, Modelo: Nika",fruit_type="mythical_zoan",haki=("armament","observation","conqueror"),archetype="DPS versátil",skill="conqueror_strike",passive="gear_five",bounty=3_000_000_000,origin="East Blue",description="Yonkou que combina elasticidade, imaginação e os três tipos de Haki."),
    _c("roronoa-zoro","Roronoa Zoro","Caçador de Piratas","Piratas do Chapéu de Palha","Espadachim","⚔️",(1750,95,90,92,94),haki=("armament","observation","conqueror"),archetype="DPS físico",skill="precision_cut",damage_type="cutting",bounty=1_111_000_000,origin="East Blue",description="Mestre do Santoryu e usuário do Haki do Conquistador avançado."),
    _c("sanji","Sanji","Perna Negra","Piratas do Chapéu de Palha","Cozinheiro","🔥",(1600,90,93,98,92),haki=("armament","observation"),archetype="DPS veloz",skill="ifrit",passive="exoskeleton",damage_type="fire",bounty=1_032_000_000,origin="North Blue",description="Velocidade extrema, exoesqueleto Germa e chamas azuis do Ifrit Jambe."),
    _c("jinbe","Jinbe","Cavaleiro do Mar","Piratas do Chapéu de Palha","Timoneiro","🌊",(1650,92,95,82,90),haki=("armament","observation"),archetype="Tank",skill="water_shock",passive="water_master",damage_type="water",bounty=1_100_000_000,origin="Ilha dos Homens-Peixe",description="Mestre do Gyojin Karate, especialmente perigoso quando há água."),
    _c("nico-robin","Nico Robin","Criança Demônio","Piratas do Chapéu de Palha","Arqueóloga","📜",(1000,78,80,75,93),fruit="Hana Hana no Mi",fruit_type="paramecia",archetype="Controle",skill="clutch",bounty=930_000_000,origin="West Blue",description="Especialista em imobilização, chaves articulares e espionagem."),
    _c("franky","Franky","Ciborgue","Piratas do Chapéu de Palha","Carpinteiro","🤖",(1300,88,92,65,85),archetype="Tank",skill="radical_beam",passive="cyborg_armor",damage_type="energy",bounty=394_000_000,origin="South Blue",description="Ciborgue equipado com lasers, foguetes e armaduras pesadas."),
    _c("brook","Brook","Soul King","Piratas do Chapéu de Palha","Músico","🎻",(950,75,70,94,88),fruit="Yomi Yomi no Mi",fruit_type="paramecia",archetype="Controle veloz",skill="soul_freeze",damage_type="ice",bounty=383_000_000,origin="West Blue",description="Espadachim extremamente leve que combina gelo e música ilusória."),
    _c("chopper","Tony Tony Chopper","Amante de Algodão Doce","Piratas do Chapéu de Palha","Médico","🦌",(1100,82,85,78,80),fruit="Hito Hito no Mi",fruit_type="zoan",archetype="Suporte",skill=("medical_care","monster_point"),passive="doctor",bounty=1_000,origin="Grand Line",description="Médico capaz de curar aliados, alternar formas e assumir o Monster Point."),
    _c("nami","Nami","Gata Ladra","Piratas do Chapéu de Palha","Navegadora","⛈️",(600,50,55,70,86),archetype="Suporte",skill="thunderbolt",passive="weather_boost",damage_type="lightning",bounty=366_000_000,origin="East Blue",description="Controla o clima com o Clima-Tact e conta com o poder de Zeus."),
    _c("usopp","Usopp","God Usopp","Piratas do Chapéu de Palha","Atirador","🎯",(750,55,75,68,88),haki=("observation",),archetype="Controle",skill="pop_green",passive="last_stand",damage_type="projectile",bounty=500_000_000,origin="East Blue",description="Atirador inventivo que vence pela preparação e precisão."),
    _c("shanks","Shanks","Ruivo","Piratas do Ruivo","Capitão","🗡️",(1900,98,94,98,100),haki=("armament","observation","conqueror"),archetype="Lenda",skill="divine_departure",passive="observation_killer",playable=False,damage_type="cutting",bounty=4_048_900_000,origin="West Blue",description="Yonkou sem Akuma no Mi que alcançou o topo por esgrima e Haki absolutos."),
    _c("whitebeard","Edward Newgate","Barba Branca","Piratas do Barba Branca","Capitão","🌋",(2500,100,96,75,95),fruit="Gura Gura no Mi",fruit_type="paramecia",haki=("armament","observation","conqueror"),archetype="Lenda",skill="quake",passive="worlds_strongest",playable=False,damage_type="quake",bounty=5_046_000_000,description="O homem capaz de provocar terremotos e rivalizar com Gol D. Roger."),
    _c("marco","Marco","A Fênix","Piratas do Barba Branca","Ex-comandante","🪽",(2100,86,98,93,88),fruit="Tori Tori no Mi, Modelo: Fênix",fruit_type="mythical_zoan",haki=("armament","observation"),archetype="Suporte",skill="phoenix_flame",passive="regeneration",damage_type="fire",bounty=1_374_000_000,description="Fênix mítica que regenera ferimentos e sustenta toda a equipe."),
    _c("ace","Portgas D. Ace","Punhos de Fogo","Piratas do Barba Branca","Comandante","🔥",(1150,85,78,88,84),fruit="Mera Mera no Mi",fruit_type="logia",haki=("armament","observation","conqueror"),archetype="DPS de área",skill="fire_fist",damage_type="fire",bounty=550_000_000,origin="South Blue",weaknesses=("water","seastone"),description="Usuário da Logia do fogo com enorme poder de área."),
    _c("blackbeard","Marshall D. Teach","Barba Negra","Piratas do Barba Negra","Capitão","🌑",(2200,98,88,70,82),fruit="Yami Yami no Mi + Gura Gura no Mi",fruit_type="special",haki=("armament","observation"),archetype="Chefe",skill="dark_vortex",passive="double_damage_taken",playable=False,damage_type="darkness",bounty=3_996_000_000,description="Único usuário conhecido de duas Akuma no Mi; anula poderes e destrói o terreno."),
    _c("kuzan","Kuzan","Aokiji","Piratas do Barba Negra","Capitão Titânico","🧊",(1800,95,95,91,97),fruit="Hie Hie no Mi",fruit_type="logia",haki=("armament","observation"),archetype="Controle",skill="ice_age",damage_type="ice",bounty=3_000_000_000,weaknesses=("seastone",),description="Ex-Almirante que domina o campo com gelo e técnica refinada."),
    _c("mihawk","Dracule Mihawk","Olhos de Falcão","Cross Guild","Espadachim","🦅",(1850,99,93,95,100),haki=("armament","observation"),archetype="Lenda",skill="world_cut",passive="perfect_edge",playable=False,damage_type="cutting",bounty=3_590_000_000,description="O melhor espadachim do mundo, preciso e extremamente eficiente."),
    _c("crocodile","Crocodile","Rei do Deserto","Cross Guild","Oficial-chefe","🏜️",(1200,83,85,78,89),fruit="Suna Suna no Mi",fruit_type="logia",haki=(),archetype="Controle",skill="desert",passive="dehydrate",damage_type="sand",bounty=1_965_000_000,weaknesses=("water","seastone"),description="Lutador calculista que usa areia, desidratação e o próprio ambiente."),
    _c("buggy","Buggy","Palhaço Estrela","Cross Guild","Figura de proa","🎪",(800,40,80,55,60),fruit="Bara Bara no Mi",fruit_type="paramecia",archetype="Especialista",skill="buggy_ball",passive="cut_immunity",damage_type="explosive",bounty=3_189_000_000,immunities=("cutting",),description="Completamente imune a dano cortante graças à Bara Bara no Mi."),
    _c("trafalgar-law","Trafalgar D. Water Law","Cirurgião da Morte","Piratas Heart","Capitão e médico","🫀",(1350,84,82,88,94),fruit="Ope Ope no Mi",fruit_type="paramecia",haki=("armament","observation"),archetype="Controle",skill="room",passive="surgeon",damage_type="spatial",bounty=3_000_000_000,origin="North Blue",description="Remodela o espaço e causa dano interno, mas consome muita energia."),
    _c("eustass-kid","Eustass Kid","Capitão Kid","Piratas Kid","Capitão","🧲",(1600,92,93,80,82),fruit="Jiki Jiki no Mi",fruit_type="paramecia",haki=("armament","observation","conqueror"),archetype="Tank",skill="damned_punk",damage_type="magnetic",bounty=3_000_000_000,origin="South Blue",description="Tanque de guerra que molda metal e dispara canhões eletromagnéticos."),
    _c("garp","Monkey D. Garp","Herói da Marinha","Marinha","Vice-Almirante","👊",(1900,99,95,90,96),haki=("armament","observation","conqueror"),archetype="Lenda",skill="galaxy_impact",passive="iron_fist",playable=False,damage_type="blunt",description="Herói lendário que combate com socos e Haki devastador."),
    _c("koby","Koby","Herói da Nova Geração","Marinha","Capitão","⚓",(1100,84,82,92,86),haki=("armament","observation"),archetype="DPS veloz",skill="honesty",damage_type="blunt",description="Discípulo de Garp com velocidade, técnica e enorme potencial."),
    _c("sabo","Sabo","Imperador das Chamas","Exército Revolucionário","Chefe de Estado-Maior","🐲",(1450,90,87,91,90),fruit="Mera Mera no Mi",fruit_type="logia",haki=("armament","observation"),archetype="DPS técnico",skill="dragon_claw",damage_type="fire",weaknesses=("water","seastone"),description="Combina chamas com as artes marciais destrutivas do Ryusoken."),
    _c("rayleigh","Silvers Rayleigh","Rei das Trevas","Piratas do Roger","Ex-imediato","🌒",(1500,94,92,95,98),haki=("armament","observation","conqueror"),archetype="DPS técnico",skill="dark_king",passive="veteran",damage_type="cutting",description="Mestre dos três Hakis, limitado apenas pela energia da idade."),
    _c("yamato","Yamato","Princesa Oni","Aliados de Wano","Samurai","🐺",(1700,94,95,90,86),fruit="Inu Inu no Mi, Modelo: Okuchi no Makami",fruit_type="mythical_zoan",haki=("armament","observation","conqueror"),archetype="Tank",skill="divine_glacier",damage_type="ice",description="Durabilidade mítica, gelo, kanabo e Haki do Conquistador."),
    _c("katakuri","Charlotte Katakuri","Katakuri da Farinha","Piratas da Big Mom","Comandante Doce","🍩",(1400,88,89,94,95),fruit="Mochi Mochi no Mi",fruit_type="special_paramecia",haki=("armament","observation","conqueror"),archetype="Controle",skill="future_mochi",passive="future_sight",description="Vê o futuro e molda mochi para atacar, prender e esquivar."),
    _c("boa-hancock","Boa Hancock","Imperatriz Pirata","Piratas Kuja","Capitã","💘",(1250,87,84,90,91),fruit="Mero Mero no Mi",fruit_type="paramecia",haki=("armament","observation","conqueror"),archetype="Controle",skill="perfume_femur",passive="petrifying_beauty",damage_type="blunt",bounty=1_659_000_000,description="Petrifica alvos e combina a fruta com chutes imbuídos em Haki."),
    _c("doflamingo","Donquixote Doflamingo","Joker","Piratas Donquixote","Ex-capitão","🕶️",(1350,85,88,87,92),fruit="Ito Ito no Mi",fruit_type="paramecia",haki=("armament","observation","conqueror"),archetype="Controle",skill="parasite",passive="organ_stitch",damage_type="cutting",bounty=340_000_000,description="Manipula fios, controla pessoas e remenda os próprios órgãos."),
    _c("kozuki-oden","Kozuki Oden","Samurai Lendário","Clã Kozuki","Daimyo","🍢",(1850,97,93,92,96),haki=("armament","observation","conqueror"),archetype="DPS físico",skill="togen",passive="boiling_resolve",damage_type="cutting",description="Samurai de resistência monstruosa que marcou Kaido para sempre."),
    _c("rob-lucci","Rob Lucci","Arma de Massacre","CP0","Agente","🐆",(1450,91,90,95,92),fruit="Neko Neko no Mi, Modelo: Leopardo",fruit_type="zoan",haki=("armament","observation"),archetype="DPS veloz",skill="rokuogan",playable=False,damage_type="blunt",description="Agente de elite especialista em Rokushiki."),
    _c("enel","Enel","Deus de Skypiea","Forças de Enel","Governante","⚡",(1350,88,78,99,96),fruit="Goro Goro no Mi",fruit_type="logia",haki=("observation",),archetype="Chefe",skill="el_thor",playable=False,damage_type="lightning",weaknesses=("rubber","seastone"),description="Logia elétrica com velocidade extrema e percepção ampliada."),
    _c("kaido","Kaido","Rei das Feras","Piratas das Feras","Capitão","🐉",(2600,100,100,88,94),fruit="Uo Uo no Mi, Modelo: Seiryu",fruit_type="mythical_zoan",haki=("armament","observation","conqueror"),archetype="Chefe",skill="thunder_bagua",passive="invulnerable_scales",playable=False,damage_type="blunt",bounty=4_611_100_000,description="Uma muralha viva com força, Haki e durabilidade absurdos."),
]

CREWS = []
for character in CHARACTERS:
    if not any(crew["name"] == character["crew"] for crew in CREWS):
        CREWS.append({"name": character["crew"], "captain": next((c["name"] for c in CHARACTERS if c["crew"] == character["crew"] and c["role"] in {"Capitão","Capitã"}), "Não informado"), "ship": "Arquivo reservado", "symbol": character["symbol"], "description": f"Registros conhecidos de {character['crew']}."})

TOWER = [
    {"enemy":"rob-lucci","name":"Portão da Justiça","reward":2200,"hint":"Velocidade e dano interno testam sua primeira formação."},
    {"enemy":"crocodile","name":"Tempestade de Areia","reward":3200,"hint":"Logia: use Haki, água ou outra fraqueza válida."},
    {"enemy":"enel","name":"Julgamento do Céu","reward":4500,"hint":"A borracha é uma resposta natural; Haki também funciona."},
    {"enemy":"kaido","name":"A Ilha do Dragão","reward":7000,"hint":"Durabilidade extrema exige dano consistente e controle."},
    {"enemy":"blackbeard","name":"O Abismo de Duas Frutas","reward":10000,"hint":"Chefe final: ele silencia habilidades e destrói defesas."},
]

SYNERGIES = {
    frozenset(("monkey-d-luffy","roronoa-zoro","sanji")): {"name":"Trio Monstro","stat":"strength","bonus":.10},
    frozenset(("garp","koby","kuzan")): {"name":"Justiça Inquebrável","stat":"defense","bonus":.10},
    frozenset(("buggy","crocodile","mihawk")): {"name":"Cross Guild","stat":"technique","bonus":.15},
}


def get_character(slug): return next((c for c in CHARACTERS if c["slug"] == slug), None)
def crew_members(name): return [c for c in CHARACTERS if c["crew"] == name]
def get_skill(skill_id): return SKILLS[skill_id]
