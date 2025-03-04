import math
import random
import os
import pygame
import pygame.mixer

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Woman game")

# Paths

current_path = os.path.dirname(os.path.abspath(__file__))

def get_image_path(filename):
    return os.path.join(current_path, "Assets", "Images", filename)

def get_sound_path(filename):
    return os.path.join(current_path, "Assets", "Sounds", filename)
# Load assets
background = pygame.image.load(get_image_path("bg.png"))
pygame.mixer.music.load(get_sound_path("bg.mp3"))
pygame.mixer.music.play(-1)

icon = pygame.image.load(get_image_path("logo_company.png"))
pygame.display.set_icon(icon)

# Player setup
playerImg = pygame.image.load(get_image_path('sakura.png'))
playerX, playerY = 370, 500
playerX_change = 0

# KO screen
koImg = pygame.image.load(get_image_path('ko.png'))
koX, koY = 200, 150

# Enemy setup
enemyImg, enemyX, enemyY, enemyX_change, enemyY_change = [], [], [], [], []
num_of_enemies = 3  # Start with 3 enemies
max_enemies = 10  # Max number of enemies

enemy_images = [
    'sasuke.png', 'naruto.png', 'sai.png', 'gaara.png', 'neji.png',
    'haku.png', 'shikamaru.png', 'itachi.png', 'kiba.png', 'lee.png'
]
available_images = enemy_images.copy()

def spawn_enemy():
    """Spawn new enemies but don't have the same image and aren't too close together."""
    global available_images
    
    if len(enemyX) >= max_enemies:
        return  
    
    spawn_x = random.randint(100, 700)
    while any(abs(spawn_x - x) < 80 for x in enemyX):
        spawn_x = random.randint(100, 700)
    
    if not available_images:
        available_images = enemy_images.copy()
    
    random_enemy = available_images.pop(random.randint(0, len(available_images) - 1))
    
    enemyImg.append(pygame.image.load(get_image_path(random_enemy)))
    enemyX.append(spawn_x)
    enemyY.append(random.randint(50, 120))
    enemyX_change.append(random.uniform(1.5, 2.5))
    enemyY_change.append(20)

# Spawn initial enemies
for _ in range(num_of_enemies):
    spawn_enemy()

# Bullet setup
bulletImg = pygame.image.load(get_image_path('bullet_arrow.png'))
bulletX, bulletY = 0, 450
bullet_state = "ready"

# Score setup
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (253, 63, 190))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def ko(x, y):
    screen.blit(koImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    return math.dist((enemyX, enemyY), (bulletX, bulletY)) < 20

# Clock for FPS control
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound = pygame.mixer.Sound(get_sound_path("laser.wav"))
                bulletSound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0

    # Increse enemy count when score < 50
    if score_value < 50:
        new_enemy_count = min(3 + score_value // 10, max_enemies)
        while len(enemyX) < new_enemy_count:
            spawn_enemy()
    
    # Increase enemy speed when score >= 50
    enemy_speed = 1.5 + (score_value // 10) * 0.2 if score_value < 50 else 3.5

    playerX = max(0, min(playerX + playerX_change, 736))

    for i in range(len(enemyX)):
        if enemyY[i] > 440:
            for j in range(len(enemyX)):
                enemyY[j] = 2000
            ko(koX, koY)
            pygame.mixer.music.stop()
            pygame.mixer.Sound(get_sound_path("ko.wav")).play(0)
            pygame.mixer.Sound(get_sound_path("diebg.wav")).play(-1)
            break

        enemyX[i] += enemyX_change[i] * enemy_speed
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY) and bullet_state == "fire":
            pygame.mixer.Sound(get_sound_path("explosion.wav")).play(0)
            bulletY = 450
            bullet_state = "ready"
            score_value += 1
            
            spawn_x = random.randint(100, 700)
            while any(abs(spawn_x - x) < 80 for x in enemyX):
                spawn_x = random.randint(100, 700)
            
            enemyX[i] = spawn_x
            enemyY[i] = random.randint(50, 120)

        enemy(enemyX[i], enemyY[i], i)

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= 10
        if bulletY <= 0:
            bulletY = 450
            bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    clock.tick(60)
