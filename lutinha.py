import pygame
import random 
import time


# Inicia PyGame (e sons) 
pygame.init()
pygame.mixer.init()

# Sons 

    #Fundo
pygame.mixer.music.load("sons/som_fundo.mp3")
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)

    #Efeitos 
som_ataque_espada = pygame.mixer.Sound("sons/som_espada.mp3")
som_ataque_flecha = pygame.mixer.Sound ("sons/som_flecha.wav")
som_botao = pygame.mixer.Sound("sons/som_botao_e_flecha.mp3")
som_vida = pygame.mixer.Sound("sons/som_cogumelo.mp3")
som_pega_espada = pygame.mixer.Sound("sons/som_virou_espada.wav")
som_pega_arco = pygame.mixer.Sound("sons/som_botao_e_flecha.mp3") 
som_ganha = pygame.mixer.Sound("sons/som_vitoria.wav")


som_ataque_espada.set_volume(0.1)
som_ataque_flecha.set_volume(0.1)
som_vida.set_volume(0.1)
som_pega_espada.set_volume(0.15)
som_ganha.set_volume(0.2)



# Gera tela principal
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pixel Clash")

# Determina o fundo (6 opções de fundo que serão escolhidas de forma aleatória)
opcoes_de_fundos = [
    "imagens/fundo1.png",
    "imagens/fundo2.png",
    "imagens/fundo3.png",
    "imagens/fundo4.png",
    "imagens/fundo5.png",
    "imagens/fundo6.png",
    "imagens/fundo7.png",
    "imagens/fundo8.png"
]

fundo_escolhido = random.choice(opcoes_de_fundos)
fundo_original = pygame.image.load(fundo_escolhido).convert()
fundo = pygame.transform.scale(fundo_original, (largura, altura))


# Tela inicial e botão start 
fundo_inicial = pygame.image.load("imagens/fundo_inicial.png").convert()
fundo_inicial = pygame.transform.scale(fundo_inicial, (largura, altura))
botao_start = pygame.Rect(340, 450, 250, 90)  

# Botões e tela info 
botao_info = pygame.Rect(410, 205, 125, 100)  
botao_info_img = pygame.image.load("imagens/botao_info.png")
botao_info_img = pygame.transform.scale(botao_info_img, (125, 100))

botao_back = pygame.Rect(2, 10, 125, 100)  
botao_back_img = pygame.image.load("imagens/botao_back.png")
botao_back_img = pygame.transform.scale(botao_back_img, (125, 100))

tela_info = pygame.image.load("imagens/info.png").convert() 
tela_info = pygame.transform.scale(tela_info, (largura, altura))


#Imagem flecha 
flecha_img = pygame.image.load("imagens/flecha.png").convert_alpha()
flecha_img = pygame.transform.scale(flecha_img, (60, 30)) #ajuste tamanho 

# Imagem plataforma
plataforma_img = pygame.image.load("imagens/plataforma.png").convert_alpha()

# Parâmetros do personagem
largura_personagem = 50
altura_personagem = 50

vida1, vida2 = 100, 100  # Vida inicial dos dois jogadores
largura_barra = 300
altura_barra = 20


# Definir a altura do chão (baseado na altura da tela e na altura dos personagens)
chao = altura - 100  # 100 é a altura do chão (onde os personagens vão "pisar")

# Posições iniciais dos personagens
x1, y1 = 600, chao - altura_personagem  # Posição do jogador 1 (setas)
x2, y2 = 300, chao - altura_personagem  # Posição do jogador 2 (WASD)

velocidade = 5
gravidade = 1
forca_pulo = 15
pulo1, pulo2 = False, False
velocidade_pulo1, velocidade_pulo2 = 0, 0

# Direção atual dos jogadores (1 = direita, -1 = esquerda)
direcao1 = -1
direcao2 = 1

# Flags de controle para impedir múltiplos tiros com tecla pressionada
pode_atirar_p1 = True
pode_atirar_p2 = True
# Flags de controle para impedir múltiplos ataques com faca segurando a tecla
pode_usar_faca_p1 = True
pode_usar_faca_p2 = True

# Criação do relógio para controlar FPS
clock = pygame.time.Clock()

# 6 opções de plataformas (x, y, largura, altura), que serão escolhidas de forma aleatória      
plataformas1 = [
    pygame.Rect(200, 400, 400, 20),
    pygame.Rect(500, 300, 200, 20),
    pygame.Rect(750, 450, 120, 20),
    pygame.Rect(100, 270, 100, 20),
    pygame.Rect(300, 200, 150, 20),
    pygame.Rect(600, 120, 280, 20)
]

plataformas2 = [
    pygame.Rect(70, 270, 300, 20),
    pygame.Rect(690, 370, 250, 20),
    pygame.Rect(250, 410, 150, 20),
    pygame.Rect(600, 210, 200, 20),
    pygame.Rect(330, 130, 180, 20)
]

plataformas3 = [
    pygame.Rect(100, 400, 250, 20),
    pygame.Rect(700, 400, 250, 20),
    pygame.Rect(100, 120, 250, 20),
    pygame.Rect(700, 120, 250, 20),
    pygame.Rect(270, 260, 500, 20)
]

plataformas4 = [
    pygame.Rect(200, 400, 120, 20),
    pygame.Rect(450, 310, 120, 20),
    pygame.Rect(700, 230, 120, 20),
    pygame.Rect(320, 160, 120, 20),
    pygame.Rect(550, 100, 120, 20),
    pygame.Rect(120, 280, 120, 20),
    pygame.Rect(700, 390, 120, 20)
]

plataformas5 = [
    pygame.Rect(200, 400, 200, 20),
    pygame.Rect(650, 350, 200, 20),
    pygame.Rect(400, 250, 200, 20),
    pygame.Rect(150, 190, 150, 20),
    pygame.Rect(600, 100, 150, 20)
]

plataformas6 = [
    pygame.Rect(190, 430, 200, 20),
    pygame.Rect(380, 350, 200, 20),
    pygame.Rect(720, 300, 200, 20),
    pygame.Rect(520, 220, 200, 20),
    pygame.Rect(290, 120, 200, 20),
    pygame.Rect(120, 240, 200, 20)
]

opcoes_de_plataformas = [plataformas1, plataformas2, plataformas3, plataformas4, plataformas5, plataformas6]

plataformas = random.choice(opcoes_de_plataformas)

itens = []  # Lista de itens no mapa

# Poderes ativos com tempo de expiração
poderes = {
    "p1_faca": 0,
    "p1_arma": 0,
    "p2_faca": 0,
    "p2_arma": 0,
}

andando_sprite_espada_azul = False
andando_sprite_espada_amarelo = False
atacando_sprite_espada_azul = False
atacando_sprite_espada_amarelo = False

andando_sprite_arco_azul = False
andando_sprite_arco_amarelo = False
atacando_sprite_arco_azul = False
atacando_sprite_arco_amarelo = False

tempo_ataque_p1 = 0
tempo_ataque_p2 = 0

duracao_ataque = 300  # em milissegundos

# Lista de tiros ativos
tiros = []

# Parâmetros para animação 
indice_animacao1 = 0
indice_animacao2 = 0
tempo_ultima_animacao = 0
intervalo_animacao = 100  # milissegundos entre quadros

# Ícones dos itens
faca_img = pygame.image.load("imagens/espada.png").convert_alpha()
faca_img = pygame.transform.scale(faca_img, (55, 55)) #ajuste tamanho 

arma_img = pygame.image.load("imagens/arco.png").convert_alpha()
arma_img = pygame.transform.scale(arma_img, (45, 45)) #ajuste tamanho 

fruta_img = pygame.image.load("imagens/fruta.png").convert_alpha()
fruta_img = pygame.transform.scale(fruta_img, (70, 70)) #ajuste tamanho 

# -------------------------------------FUNÇÕES------------------------------------------------

# Função para mostrar a tela inicial 
def mostrar_tela_inicial():
    """
    Exibe a tela inicial do jogo com opções de iniciar ou ver informações.
    Espera interação do usuário para continuar.
    """
    while True:
        tela.blit(fundo_inicial, (0, 0))  # Desenha a imagem na tela
        tela.blit(botao_info_img, botao_info.topleft) # Desenha botão de start 

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_info.collidepoint(evento.pos):
                    som_botao.play()
                    mostrar_tela_info()
                if botao_start.collidepoint(evento.pos):
                    som_botao.play()
                    return  # Sai da tela inicial

        pygame.display.flip()
        clock.tick(60)

def mostrar_tela_info():
    """
    Exibe a tela com informações do jogo.
    Retorna à tela inicial ao clicar no botão de voltar.
    """
    while True: 
        tela.blit(tela_info, (0, 0))  # Desenha a imagem na tela
        tela.blit(botao_back_img, botao_back.topleft) # Desenha botão back 

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_back.collidepoint(evento.pos):
                    som_botao.play()
                    return 
                
        pygame.display.flip()
        clock.tick(60)



# Função para mostrar tela de vitória 
def mostrar_tela_vitoria(vencedor):
    """
    Exibe a tela de vitória para o jogador vencedor e aguarda o clique para reiniciar o jogo.

    Parâmetros:
    vencedor (str): "amarelo" ou outro valor para azul, indicando quem venceu.
    """
    if vencedor == "amarelo":
        fundo_vitoria = pygame.image.load("imagens/fundo_final_amarelo.png").convert()
        fundo_vitoria = pygame.transform.scale(fundo_vitoria, (largura, altura))

    else:
        fundo_vitoria = pygame.image.load("imagens/fundo_final_azul.png").convert()
        fundo_vitoria = pygame.transform.scale(fundo_vitoria, (largura, altura))

    botao_restart = pygame.Rect(340, 450, 250, 90)  # área do botão na imagem

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_restart.collidepoint(evento.pos):
                    som_botao.play()
                    return  # Sai da tela de vitória e reinicia o jogo
            
        tela.blit(fundo_vitoria, (0, 0))
        pygame.display.flip()
        clock.tick(60)

# Função para reiniciar o jogo (zera todas as variáveis)
def reiniciar_jogo():
    """
    Reinicia o estado do jogo, redefinindo posições, vidas, plataformas,
    itens, poderes e animações dos personagens.
    """
    global x1, y1, vida1, pulo1, velocidade_pulo1, andando_sprite_espada_amarelo, andando_sprite_arco_amarelo
    global x2, y2, vida2, pulo2, velocidade_pulo2, andando_sprite_espada_azul, andando_sprite_arco_azul
    global poderes, itens, tiros, tempo_ataque_p1, tempo_ataque_p2
    global indice_animacao1, indice_animacao2, tempo_ultima_animacao
    global fundo, plataformas

    # fundo aleatorio novamente 
    fundo_escolhido = random.choice(opcoes_de_fundos)
    fundo_original = pygame.image.load(fundo_escolhido).convert()
    fundo = pygame.transform.scale(fundo_original, (largura, altura))
    
    # plataformas aleatorias novamente 
    plataformas = random.choice(opcoes_de_plataformas)
    
    # Posicoes iniciais
    x1, y1 = 600, chao - altura_personagem
    x2, y2 = 300, chao - altura_personagem

    # Vidas
    vida1 = 100
    vida2 = 100

    # Pulos
    pulo1 = False
    pulo2 = False
    velocidade_pulo1 = 0
    velocidade_pulo2 = 0

    # Flags de animação
    andando_sprite_espada_amarelo = False
    andando_sprite_arco_amarelo = False
    andando_sprite_espada_azul = False
    andando_sprite_arco_azul = False

    # Poderes com tempo expirado (0 = sem poder)
    poderes = {
        "p1_faca": 0,
        "p1_arma": 0,
        "p2_faca": 0,
        "p2_arma": 0,
    }

    # Limpar listas de itens e tiros
    itens.clear()
    tiros.clear()

    # Tempos de ataque resetados
    tempo_ataque_p1 = 0
    tempo_ataque_p2 = 0

    # Animação
    indice_animacao1 = 0
    indice_animacao2 = 0
    tempo_ultima_animacao = pygame.time.get_ticks()
 

# Função para desenhar barras de vida
def desenhar_barras_de_vida():
    """
    Desenha as barras de vida de ambos os jogadores na tela, cada uma com a cor do personagem. 
    """
    # Jogador 1 (azul)
    pygame.draw.rect(tela, (255, 0, 0), (50, 30, largura_barra, altura_barra))  # Barra vermelha (fundo)
    pygame.draw.rect(tela, (80, 150, 255), (50, 30, largura_barra * (vida2 / 100), altura_barra))  # Vida

    # Jogador 2 (amarelo)
    pygame.draw.rect(tela, (255, 0, 0), (largura - 50 - largura_barra, 30, largura_barra, altura_barra))  # Fundo
    pygame.draw.rect(tela, (255, 219, 88), (largura - 50 - largura_barra, 30, largura_barra * (vida1 / 100), altura_barra))

# Função para ver se o personagem está no chão/plataforma
def esta_no_chao_ou_plataforma(x, y):
    """
    Verifica se o personagem está no chão ou em uma plataforma.

    Parâmetros:
    x (int): Posição x do personagem.
    y (int): Posição y do personagem.

    Retorna:
    bool: True se estiver no chão ou em uma plataforma, False caso contrário.
    """
    rect = pygame.Rect(x, y, largura_personagem, altura_personagem)
    if y + altura_personagem >= chao:
        return True
    for plataforma in plataformas:
        if rect.colliderect(plataforma.move(0, -1)):  # Pequeno ajuste para evitar bug visual
            return True
    return False

def spawn_item():
    """
    Gera um novo item (faca/espada, arma/arco ou fruta) em uma posição aleatória,
    adicionando na lista de itens.
    """
    tipo = random.choice(["faca", "arma", "fruta"])
    x = random.randint(50, largura - 70)
    y = random.randint(100, chao - 30)
    itens.append({"tipo": tipo, "rect": pygame.Rect(x, y, 20, 20)})

def desenhar_itens():
    """
    Desenha todos os itens (faca/espada, arma/arco, fruta) ativos na tela.
    """
    for item in itens:
        if item["tipo"] == "faca":
            tela.blit(faca_img, item["rect"])
        elif item["tipo"] == "arma":
            tela.blit(arma_img, item["rect"])
        elif item["tipo"] == "fruta":
            tela.blit(fruta_img, item["rect"])

# Carrega e divide os sprites em listas de quadros (TRECHO GERADO PELO CHATGPT)
def carregar_sprites(nome_arquivo):
    """
    Carrega uma spritesheet e divide em uma lista de 6 quadros (frames).

    Parâmetros:
    nome_arquivo (str): Caminho para o arquivo de imagem da spritesheet.

    Retorna:
    list: Lista contendo os 6 quadros da animação como superfícies Pygame.
    """
    imagem = pygame.image.load(nome_arquivo).convert_alpha()
    largura_quadro = imagem.get_width() // 6
    altura_quadro = imagem.get_height()
    return [imagem.subsurface(pygame.Rect(i * largura_quadro, 0, largura_quadro, altura_quadro)) for i in range(6)]

sprites_amarelo = carregar_sprites("imagens/personagem_amarelo.png")
sprites_azul = carregar_sprites("imagens/personagem_azul.png")

sprites_amarelo_espada_andando = carregar_sprites("imagens/espada_amarelo_andando.png")
sprites_azul_espada_andando = carregar_sprites("imagens/espada_azul_andando.png")
sprites_amarelo_espada_atacando = carregar_sprites("imagens/espada_amarelo_atacando.png")
sprites_azul_espada_atacando = carregar_sprites("imagens/espada_azul_atacando.png")

sprites_amarelo_arco_andando = carregar_sprites("imagens/arqueiro_amarelo_andando.png")
sprites_azul_arco_andando= carregar_sprites("imagens/arqueiro_azul_andando.png")
sprites_amarelo_arco_atacando = carregar_sprites("imagens/arqueiro_amarelo_atacando.png")
sprites_azul_arco_atacando= carregar_sprites("imagens/arqueiro_azul_atacando.png")


#--------------------------------------------------------------------------------------------------------
# Loop do jogo
game = True

# Puxa tela inicial 
mostrar_tela_inicial()

while game:
    # Processa os eventos
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Atirar jogador 1
                if event.key == pygame.K_l and poderes["p1_arma"] > time.time() and pode_atirar_p1:
                    tiros.append({
                        "x": x1 + (largura_personagem if direcao1 == 1 else 0),
                        "y": y1 + altura_personagem // 2,
                        "direcao": direcao1,
                        "dono": 1
                    })
                    pode_atirar_p1 = False
                    tempo_ataque_p1 = pygame.time.get_ticks()  # inicia tempo de ataque
                    som_ataque_flecha.play()

                # Atirar jogador 2
                if event.key == pygame.K_f and poderes["p2_arma"] > time.time() and pode_atirar_p2:
                    tiros.append({
                        "x": x2 + (largura_personagem if direcao2 == 1 else 0),
                        "y": y2 + altura_personagem // 2,
                        "direcao": direcao2,
                        "dono": 2
                    })
                    pode_atirar_p2 = False
                    tempo_ataque_p2 = pygame.time.get_ticks()  # inicia tempo de ataque
                    som_ataque_flecha.play()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_l:
                        pode_atirar_p1 = True
                    if event.key == pygame.K_f:
                        pode_atirar_p2 = True

                # Ataque com faca - jogador 1
                if event.key == pygame.K_l and poderes["p1_faca"] > time.time() and pode_usar_faca_p1:
                    if abs(x1 - x2) < distancia_ataque and abs(y1 - y2) < altura_personagem:
                        vida2 = max(0, vida2 - dano_faca)
                    pode_usar_faca_p1 = False
                    tempo_ataque_p1 = pygame.time.get_ticks()  # inicia tempo de ataque
                    som_ataque_espada.play()

                # Ataque com faca - jogador 2
                if event.key == pygame.K_f and poderes["p2_faca"] > time.time() and pode_usar_faca_p2:
                    if abs(x2 - x1) < distancia_ataque and abs(y2 - y1) < altura_personagem:
                        vida1 = max(0, vida1 - dano_faca)
                    pode_usar_faca_p2 = False
                    tempo_ataque_p2 = pygame.time.get_ticks()  # inicia tempo de ataque
                    som_ataque_espada.play()

                if event.key == pygame.K_l:
                    pode_atirar_p1 = True
                    pode_usar_faca_p1 = True

                if event.key == pygame.K_f:
                    pode_atirar_p2 = True
                    pode_usar_faca_p2 = True


            if event.type == pygame.QUIT:
                game = False

    # Obtém o estado das teclas
    teclas = pygame.key.get_pressed()

    # Movimentação e pulo para o jogador 1 (setas)
    if teclas[pygame.K_LEFT]:
        x1 -= velocidade
        direcao1 = -1 
    if teclas[pygame.K_RIGHT]:
        x1 += velocidade
        direcao1 = 1
    if teclas[pygame.K_UP] and not pulo1 and esta_no_chao_ou_plataforma(x1, y1):
        pulo1 = True
        velocidade_pulo1 = -forca_pulo

    # Movimentação e pulo para o jogador 2 (WASD)
    if teclas[pygame.K_a]:
        x2 -= velocidade
        direcao2 = -1
    if teclas[pygame.K_d]:
        x2 += velocidade
        direcao2 = 1 
    if teclas[pygame.K_w] and not pulo2 and esta_no_chao_ou_plataforma(x2, y2):
        pulo2 = True
        velocidade_pulo2 = -forca_pulo

     # Retângulos dos personagens
    rect1 = pygame.Rect(x1, y1, largura_personagem, altura_personagem)
    rect2 = pygame.Rect(x2, y2, largura_personagem, altura_personagem)

    # Jogador 1 - gravidade
    if pulo1 or not esta_no_chao_ou_plataforma(x1, y1 + 1):
        y1 += velocidade_pulo1
        velocidade_pulo1 += gravidade
        rect1 = pygame.Rect(x1, y1, largura_personagem, altura_personagem)

        for plataforma in plataformas:
            if rect1.colliderect(plataforma) and velocidade_pulo1 >= 0:
                y1 = plataforma.y - altura_personagem
                velocidade_pulo1 = 0
                pulo1 = False
                break
        if y1 + altura_personagem >= chao:
            y1 = chao - altura_personagem
            velocidade_pulo1 = 0
            pulo1 = False
    else:
        for plataforma in plataformas:
            if rect1.colliderect(plataforma):
                y1 = plataforma.y - altura_personagem
        velocidade_pulo1 = 0
        pulo1 = False

    # Jogador 2 - gravidade
    if pulo2 or not esta_no_chao_ou_plataforma(x2, y2 + 1):
        y2 += velocidade_pulo2
        velocidade_pulo2 += gravidade
        rect2 = pygame.Rect(x2, y2, largura_personagem, altura_personagem)

        for plataforma in plataformas:
            if rect2.colliderect(plataforma) and velocidade_pulo2 >= 0:
                y2 = plataforma.y - altura_personagem
                velocidade_pulo2 = 0
                pulo2 = False
                break
        if y2 + altura_personagem >= chao:
            y2 = chao - altura_personagem
            velocidade_pulo2 = 0
            pulo2 = False
    else:
        for plataforma in plataformas:
            if rect2.colliderect(plataforma) and velocidade_pulo2 >= 0:
                y2 = plataforma.y - altura_personagem
        velocidade_pulo2 = 0
        pulo2 = False

    # Spawn de itens aleatoios
    if random.randint(0, 300) == 0:  # chance de aparecer item
        spawn_item() 

    # Trecho para animação funcionar (próximas 10 linhas geradas pelo chatgpt)
    # Verifica se há movimento para cada jogador
    jogador1_andando = teclas[pygame.K_RIGHT] or teclas[pygame.K_LEFT]
    jogador2_andando = teclas[pygame.K_a] or teclas[pygame.K_d]

    agora_ms = pygame.time.get_ticks()
    if agora_ms - tempo_ultima_animacao > intervalo_animacao:
        if jogador1_andando or (agora_ms - tempo_ataque_p1 < duracao_ataque):
            indice_animacao1 = (indice_animacao1 + 1) % 6
        if jogador2_andando or (agora_ms - tempo_ataque_p2 < duracao_ataque):
            indice_animacao2 = (indice_animacao2 + 1) % 6
        tempo_ultima_animacao = agora_ms

    # Limites horizontais
    x1 = max(0, min(x1, largura - largura_personagem))
    x2 = max(0, min(x2, largura - largura_personagem))

    # Limites verticais (evita que bugue o pulo)
    y1 = min(y1, chao - altura_personagem)
    y2 = min(y2, chao - altura_personagem)


    # Desenha o fundo na tela
    tela.blit(fundo, (0, 0))

    # Desenha plataformas
    for plataforma in plataformas:
    # Redimensiona a imagem para o tamanho da plataforma (largura, altura) e desenha
        plataforma_img_tamanho_certo = pygame.transform.scale(plataforma_img, (plataforma.width+10, plataforma.height+170))
        tela.blit(plataforma_img_tamanho_certo, (plataforma.x-10, plataforma.y-85))
    

    # Desenha os dois personagens, barras de vida e itens

        # Jogador 1
    agora_ms = pygame.time.get_ticks()
    if agora_ms - tempo_ataque_p1 < duracao_ataque:
        if poderes["p1_faca"] > time.time():
            sprites_atuais1 = sprites_amarelo_espada_atacando
        elif poderes["p1_arma"] > time.time():
            sprites_atuais1 = sprites_amarelo_arco_atacando
    elif andando_sprite_arco_amarelo:
        sprites_atuais1 = sprites_amarelo_arco_andando
    elif andando_sprite_espada_amarelo:
        sprites_atuais1 = sprites_amarelo_espada_andando 
    else: 
         sprites_atuais1 = sprites_amarelo 
    if jogador1_andando or (agora_ms - tempo_ataque_p1 < duracao_ataque):
        sprite1 = sprites_atuais1[indice_animacao1]
    else:
        sprite1 = sprites_atuais1[0]
    if direcao1 == -1:
        sprite1 = pygame.transform.flip(sprite1, True, False)
    sprite1_rect = sprite1.get_rect()
    tela.blit(sprite1, (x1 - sprite1_rect.width/3-10, y1 - sprite1_rect.height/3))

        # Jogador 2
    agora_ms = pygame.time.get_ticks()
    if agora_ms - tempo_ataque_p2 < duracao_ataque:
        if poderes["p2_faca"] > time.time():
            sprites_atuais2 = sprites_azul_espada_atacando
        elif poderes["p2_arma"] > time.time():
            sprites_atuais2 = sprites_azul_arco_atacando
    elif andando_sprite_arco_azul:
        sprites_atuais2 = sprites_azul_arco_andando
    elif andando_sprite_espada_azul:
        sprites_atuais2 = sprites_azul_espada_andando
    else: 
         sprites_atuais2 = sprites_azul 
    if jogador2_andando or (agora_ms - tempo_ataque_p2 < duracao_ataque):
        sprite2 = sprites_atuais2[indice_animacao2]
    else:
        sprite2 = sprites_atuais2[0]
    if direcao2 == -1:
        sprite2 = pygame.transform.flip(sprite2, True, False)
    sprite2_rect = sprite2.get_rect()
    tela.blit(sprite2, (x2 - sprite2_rect.width/3-10, y2 - sprite2_rect.height/3))


    desenhar_barras_de_vida() 
    desenhar_itens()

    # Verificar se os personagens pegaram algum item
    for item in itens[:]:
        if rect1.colliderect(item["rect"]):
            if item["tipo"] == "faca":
                poderes["p1_faca"] = time.time() + 10
                poderes["p1_arma"] = 0  # cancela o arco
                andando_sprite_espada_amarelo = True
                andando_sprite_arco_amarelo = False
                som_pega_espada.play()
            elif item["tipo"] == "arma":
                poderes["p1_arma"] = time.time() + 10
                poderes["p1_faca"] = 0  # cancela a espada
                andando_sprite_arco_amarelo = True
                andando_sprite_espada_amarelo = False
                som_pega_arco.play()
            elif item["tipo"] == "arma":
                poderes["p1_arma"] = time.time() + 10
                andando_sprite_arco_amarelo = True
            elif item["tipo"] == "fruta":
                vida1 = min(100, vida1 + 1)
                som_vida.play()
            itens.remove(item)

        elif rect2.colliderect(item["rect"]):
            if item["tipo"] == "faca":
                poderes["p2_faca"] = time.time() + 10
                poderes["p2_arma"] = 0  # cancela o arco
                andando_sprite_espada_azul = True
                andando_sprite_arco_azul = False
                som_pega_espada.play()
            elif item["tipo"] == "arma":
                poderes["p2_arma"] = time.time() + 10
                poderes["p2_faca"] = 0  # cancela a espada
                andando_sprite_arco_azul = True
                andando_sprite_espada_azul = False
                som_pega_arco.play()
            elif item["tipo"] == "fruta":
                vida2 = min(100, vida2 + 1)
                som_vida.play()
            itens.remove(item)



    # Parâmetros do ataque 

    agora = time.time()
    dano_faca = 2
    dano_tiro = 1
    distancia_ataque = 60
    vel_tiro = 10

    if poderes["p1_faca"] < agora:
        andando_sprite_espada_amarelo = False
    if poderes["p2_faca"] < agora:
        andando_sprite_espada_azul = False
    if poderes["p1_arma"] < agora:
        andando_sprite_arco_amarelo = False
    if poderes["p2_arma"] < agora:
        andando_sprite_arco_azul = False

    # Atualizar e desenhar tiros
    for tiro in tiros[:]:
        tiro["x"] += tiro["direcao"] * vel_tiro
        # Gira a imagem se a direção for para a esquerda
        if tiro["direcao"] < 0:
            flecha = pygame.transform.flip(flecha_img, True, False)
        else:
            flecha = flecha_img

        # Desenha a imagem na posição do tiro
        tela.blit(flecha, (int(tiro["x"]), int(tiro["y"])))

        if tiro["dono"] == 1 and rect2.collidepoint(tiro["x"], tiro["y"]):
            vida2 = max(0, vida2 - dano_tiro)
            tiros.remove(tiro)
        elif tiro["dono"] == 2 and rect1.collidepoint(tiro["x"], tiro["y"]):
            vida1 = max(0, vida1 - dano_tiro)
            tiros.remove(tiro)
        elif tiro["x"] < 0 or tiro["x"] > largura:
            tiros.remove(tiro)

    # Confere se o jogo acabou 
    if vida1 <= 0:
        som_ganha.play()
        mostrar_tela_vitoria("azul")
        reiniciar_jogo()  # volta o jogo pro estado inicial

    elif vida2 <= 0:
        som_ganha.play()
        mostrar_tela_vitoria("amarelo")
        reiniciar_jogo()  # volta o jogo pro estado inicial



    # Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(60)

# Finaliza o PyGame
pygame.quit()
