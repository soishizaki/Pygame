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
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Parâmetros do personagem
largura_personagem = 50
altura_personagem = 50

# Definir a altura do chão (baseado na altura da tela e na altura dos personagens)
chao = altura - 100  # 100 é a altura do chão (onde os personagens vão "pisar")

# Posições iniciais dos personagens
x1, y1 = 100, chao - altura_personagem  # Posição do jogador 1 (setas)
x2, y2 = 800, chao - altura_personagem  # Posição do jogador 2 (WASD)

velocidade = 5
gravidade = 1
forca_pulo = 15
pulo1, pulo2 = False, False
velocidade_pulo1, velocidade_pulo2 = 0, 0

# Criação do relógio para controlar FPS
clock = pygame.time.Clock()

# Função para desenhar os personagens
def desenhar_personagem(x, y, cor):
    pygame.draw.rect(tela, cor, (x, y, largura_personagem, altura_personagem))

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
    if teclas[pygame.K_DOWN]:
        y1 += velocidade
    if teclas[pygame.K_UP] and not pulo1:
        pulo1 = True
        velocidade_pulo1 = -forca_pulo

    # Movimentação e pulo para o jogador 2 (WASD)
    if teclas[pygame.K_a]:
        x2 -= velocidade
    if teclas[pygame.K_d]:
        x2 += velocidade
    if teclas[pygame.K_s]:
        y2 += velocidade
    if teclas[pygame.K_w] and not pulo2:
        pulo2 = True
        velocidade_pulo2 = -forca_pulo

    # Lógica da gravidade para o jogador 1
    if pulo1:
        y1 += velocidade_pulo1
        velocidade_pulo1 += gravidade
        if y1 >= chao - altura_personagem:  # Quando o jogador atinge o chão
            y1 = chao - altura_personagem
            pulo1 = False
            velocidade_pulo1 = 0

    # Lógica da gravidade para o jogador 2
    if pulo2:
        y2 += velocidade_pulo2
        velocidade_pulo2 += gravidade
        if y2 >= chao - altura_personagem:  # Quando o jogador atinge o chão
            y2 = chao - altura_personagem
            pulo2 = False
            velocidade_pulo2 = 0

    # Desenha o fundo na tela
    tela.blit(fundo, (0, 0))

    # Desenha os dois personagens
    desenhar_personagem(x1, y1, BRANCO)
    desenhar_personagem(x2, y2, PRETO)

    # Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(60)

# Finaliza o PyGame
pygame.quit()
