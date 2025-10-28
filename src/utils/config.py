TAMANHO_POPULACAO = 12
NUM_GERACOES = 50
TAXA_MUTACAO = 0.1
TAMANHO_CROMOSSOMO = 6  # [força, agilidade, inteligência, vitalidade, fé, carisma]

LIMITES = [
    (10, 100),  # força
    (10, 100),  # agilidade
    (10, 100),  # inteligência
    (10, 100),  # vitalidade
    (10, 100),  # fé
    (10, 100),  # carisma
]


SPRITES_POR_TIPO = {
    "Templário": ["templario_0.png", "templario_1.png", "templario_2.png"],
    "Clérigo": ["clerigo_0.png", "clerigo_1.png", "clerigo_2.png"],
    "Dragão": ["dragao_0.png", "dragao_1.png", "dragao_2.png"],
    "Guerreiro": ["guerreiro_0.png", "guerreiro_1.png"],
    "Mago": ["mago_0.png", "mago_1.png"],
}
