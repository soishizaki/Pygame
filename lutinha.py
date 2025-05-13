import pygame

# Inicia PyGame
pygame.init()

# Gera tela principal
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Lutinha")

# Determina o fundo (podemos trocar depois, é só colocar a imagem q a gente quiser com o nome 'fundo.png' na pasta imagens)
fundo_original = pygame.image.load("imagens/fundo.png").convert()
fundo = pygame.transform.scale(fundo_original, (largura, altura))

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

# Função para desenhar os personagens
def desenhar_personagem(x, y, cor):
    pygame.draw.rect(tela, cor, (x, y, largura_personagem, altura_personagem))

# Função para desenhar barras de vida
def desenhar_barras_de_vida():
    # Jogador 1 (branco)
    pygame.draw.rect(tela, (255, 0, 0), (50, 30, largura_barra, altura_barra))  # Barra vermelha (fundo)
    pygame.draw.rect(tela, (0, 255, 0), (50, 30, largura_barra * (vida1 / 100), altura_barra))  # Vida

    # Jogador 2 (preto)
    pygame.draw.rect(tela, (255, 0, 0), (largura - 50 - largura_barra, 30, largura_barra, altura_barra))  # Fundo
    pygame.draw.rect(tela, (0, 255, 0), (largura - 50 - largura_barra, 30, largura_barra * (vida2 / 100), altura_barra))

# Função para ver se o personagem está no chão/plataforma
def esta_no_chao_ou_plataforma(x, y):
    rect = pygame.Rect(x, y, largura_personagem, altura_personagem)
    if y + altura_personagem >= chao:
        return True
    for plataforma in plataformas:
        if rect.colliderect(plataforma.move(0, -1)):  # Pequeno ajuste para evitar bug visual
            return True
    return False

# Loop do jogo
game = True
while game:
    # Processa os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # Obtém o estado das teclas
    teclas = pygame.key.get_pressed()

    # Movimentação e pulo para o jogador 1 (setas)
    if teclas[pygame.K_LEFT]:
        x1 -= velocidade
    if teclas[pygame.K_RIGHT]:
        x1 += velocidade
    if teclas[pygame.K_UP] and not pulo1 and esta_no_chao_ou_plataforma(x1, y1):
        pulo1 = True
        velocidade_pulo1 = -forca_pulo

    # Movimentação e pulo para o jogador 2 (WASD)
    if teclas[pygame.K_a]:
        x2 -= velocidade
    if teclas[pygame.K_d]:
        x2 += velocidade
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
        velocidade_pulo2 = 0
        pulo2 = False

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
    

    # Desenha os dois personagens e as barras de vida
    desenhar_personagem(x1, y1, branco)
    desenhar_personagem(x2, y2, preto)
    desenhar_barras_de_vida() 

    # Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(60)

# Finaliza o PyGame
pygame.quit()
