import pygame
import random 
import time


# Inicia PyGame
pygame.init()

# Gera tela principal
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Lutinha")

# Determina o fundo (podemos trocar depois, é só colocar a imagem q a gente quiser com o nome 'fundo.png' na pasta imagens)
fundo_original = pygame.image.load("imagens/fundo.png").convert()
fundo = pygame.transform.scale(fundo_original, (largura, altura))

#Imagem flecha 
flecha_img = pygame.image.load("imagens/flecha.png").convert_alpha()
flecha_img = pygame.transform.scale(flecha_img, (60, 30)) #ajuste tamanho 


# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza = (150, 150, 150)

# Parâmetros do personagem
largura_personagem = 50
altura_personagem = 50

vida1, vida2 = 100, 100  # Vida inicial dos dois jogadores
largura_barra = 300
altura_barra = 20


# Definir a altura do chão (baseado na altura da tela e na altura dos personagens)
chao = altura - 100  # 100 é a altura do chão (onde os personagens vão "pisar")

# Posições iniciais dos personagens
x1, y1 = 800, chao - altura_personagem  # Posição do jogador 1 (setas)
x2, y2 = 100, chao - altura_personagem  # Posição do jogador 2 (WASD)

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

# Plataformas (x, y, largura, altura)         #Rect cria retângulo 
plataformas = [
    pygame.Rect(200, 400, 400, 20),
    pygame.Rect(500, 300, 200, 20),
    pygame.Rect(750, 450, 120, 20),
    pygame.Rect(100, 270, 100, 20),
    pygame.Rect(300, 200, 150, 20),
    pygame.Rect(600, 160, 280, 20)
]

itens = []  # Lista de itens no mapa

# Poderes ativos com tempo de expiração
poderes = {
    "p1_faca": 0,
    "p1_arma": 0,
    "p2_faca": 0,
    "p2_arma": 0,
}

# Lista de tiros ativos
tiros = []

# Parâmetros para animação 
indice_animacao1 = 0
indice_animacao2 = 0
tempo_ultima_animacao = 0
intervalo_animacao = 100  # milissegundos entre quadros

# Ícones dos itens (depois a gnt troca pra imagem) 
faca_img = pygame.Surface((20, 20))
faca_img.fill((200, 200, 200))  # cinza claro

arma_img = pygame.Surface((20, 20))
arma_img.fill((50, 50, 255))  # azul

fruta_img = pygame.Surface((20, 20))
fruta_img.fill((0, 255, 0))  # verde

# -------------------------------------FUNÇÕES------------------------------------------------


# Função para desenhar barras de vida
def desenhar_barras_de_vida():
    # Jogador 1 (branco)
    pygame.draw.rect(tela, (255, 0, 0), (50, 30, largura_barra, altura_barra))  # Barra vermelha (fundo)
    pygame.draw.rect(tela, (0, 255, 0), (50, 30, largura_barra * (vida2 / 100), altura_barra))  # Vida

    # Jogador 2 (preto)
    pygame.draw.rect(tela, (255, 0, 0), (largura - 50 - largura_barra, 30, largura_barra, altura_barra))  # Fundo
    pygame.draw.rect(tela, (0, 255, 0), (largura - 50 - largura_barra, 30, largura_barra * (vida1 / 100), altura_barra))

# Função para ver se o personagem está no chão/plataforma
def esta_no_chao_ou_plataforma(x, y):
    rect = pygame.Rect(x, y, largura_personagem, altura_personagem)
    if y + altura_personagem >= chao:
        return True
    for plataforma in plataformas:
        if rect.colliderect(plataforma.move(0, -1)):  # Pequeno ajuste para evitar bug visual
            return True
    return False

def spawn_item():
    tipo = random.choice(["faca", "arma", "fruta"])
    x = random.randint(50, largura - 70)
    y = random.randint(100, chao - 30)
    itens.append({"tipo": tipo, "rect": pygame.Rect(x, y, 20, 20)})

def desenhar_itens():
    for item in itens:
        if item["tipo"] == "faca":
            tela.blit(faca_img, item["rect"])
        elif item["tipo"] == "arma":
            tela.blit(arma_img, item["rect"])
        elif item["tipo"] == "fruta":
            tela.blit(fruta_img, item["rect"])

# Carrega e divide os sprites em listas de quadros (TRECHO GERADO PELO CHATGPT)
def carregar_sprites(nome_arquivo):
    imagem = pygame.image.load(nome_arquivo).convert_alpha()
    largura_quadro = imagem.get_width() // 6
    altura_quadro = imagem.get_height()
    return [imagem.subsurface(pygame.Rect(i * largura_quadro, 0, largura_quadro, altura_quadro)) for i in range(6)]

sprites_amarelo = carregar_sprites("imagens/personagem_amarelo.png")
sprites_azul = carregar_sprites("imagens/personagem_azul.png")


#--------------------------------------------------------------------------------------------------------
# Loop do jogo
game = True
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

                # Atirar jogador 2
                if event.key == pygame.K_f and poderes["p2_arma"] > time.time() and pode_atirar_p2:
                    tiros.append({
                        "x": x2 + (largura_personagem if direcao2 == 1 else 0),
                        "y": y2 + altura_personagem // 2,
                        "direcao": direcao2,
                        "dono": 2
                    })
                    pode_atirar_p2 = False

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

                # Ataque com faca - jogador 2
                if event.key == pygame.K_f and poderes["p2_faca"] > time.time() and pode_usar_faca_p2:
                    if abs(x2 - x1) < distancia_ataque and abs(y2 - y1) < altura_personagem:
                        vida1 = max(0, vida1 - dano_faca)
                    pode_usar_faca_p2 = False

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
        if jogador1_andando:
            indice_animacao1 = (indice_animacao1 + 1) % 6
        if jogador2_andando:
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

    # Desenhar plataformas
    for plataforma in plataformas:
        pygame.draw.rect(tela, cinza, plataforma)
    

    # Desenha os dois personagens, barras de vida e itens

    # Jogador 1
    sprite1 = sprites_amarelo[indice_animacao1] if jogador1_andando else sprites_amarelo[0]
    if direcao1 == -1:
        sprite1 = pygame.transform.flip(sprite1, True, False)
    sprite1_rect = sprite1.get_rect()
    tela.blit(sprite1, (x1 - sprite1_rect.width/3-10, y1 - sprite1_rect.height/3))
    # pygame.draw.rect(tela, (255,0,0), rect1)

    # Jogador 2
    sprite2 = sprites_azul[indice_animacao2] if jogador2_andando else sprites_azul[0]
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
            elif item["tipo"] == "arma":
                poderes["p1_arma"] = time.time() + 10
            elif item["tipo"] == "fruta":
                vida1 = min(100, vida1 + 1)
            itens.remove(item)

        elif rect2.colliderect(item["rect"]):
            if item["tipo"] == "faca":
                poderes["p2_faca"] = time.time() + 10
            elif item["tipo"] == "arma":
                poderes["p2_arma"] = time.time() + 10
            elif item["tipo"] == "fruta":
                vida2 = min(100, vida2 + 1)
            itens.remove(item)


    #ATAQUE (TESTE 1)

    agora = time.time()
    dano_faca = 1
    dano_tiro = 0.5
    distancia_ataque = 60
    vel_tiro = 10


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



    # Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(60)

# Finaliza o PyGame
pygame.quit()
