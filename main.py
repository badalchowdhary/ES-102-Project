import pygame
import random
pygame.init()

#Creating screen
screen = pygame.display.set_mode((800,600))

#Title and icon
pygame.display.set_caption("Ninja")
icon = pygame.image.load('ninja_icon.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('background.png')

#player
player_img = pygame.image.load('ninja.png')
ninjaX = 180
ninjaY = 530
ninjaX_change = 0


#enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(1,734))
    enemyY.append(random.randint(1,250))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#shooter
shooter_img = pygame.image.load('shooter.png')
shooterX = 0
shooterY = 530
shooterX_change = 0
shooterY_change = 2
shooter_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def player(x,y):
    screen.blit(player_img, (x,y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x,y))

def shooter(x,y):
    global shooter_state
    shooter_state = "fire"
    screen.blit(shooter_img, (x,y))

def collision(enemyX,enemyY,shooterX,shooterY):
    distance = ((shooterX - enemyX)**2 + (shooterY - enemyY)**2)**0.5
    if distance < 32:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over, (200,250))

#To hold screen
running = True
while running: 

    screen.fill((200, 250, 250))

    #background image
    screen.blit(background, (0,0))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #checking the keypress
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ninjaX_change = -0.6
            elif event.key == pygame.K_RIGHT:
                ninjaX_change =  +0.6
            
            elif event.key == pygame.K_SPACE:
                shooterX = ninjaX
                shooter(shooterX, shooterY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ninjaX_change =  0
            
        
    #moving the player
    ninjaX += ninjaX_change
    

    #defining boundaries
    if ninjaX <= 0:
        ninjaX = 0
    elif ninjaX >=736:
        ninjaX = 736

    if ninjaY <= 0:
        ninjaY = 0
    elif ninjaY >=536:
        ninjaY = 536
    
    player(ninjaX,ninjaY)

    #enemy movements
    for i in range(number_of_enemies):

        #game over
        if enemyY[i] > 480:
            for j in range(number_of_enemies):
                enemyY[j] = 800
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #check collisions
        check_collision = collision(enemyX[i],enemyY[i],shooterX,shooterY)
        if check_collision:
            shooterY = 530
            shooter_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(1,734)
            enemyY[i] = random.randint(1,250)
        
        enemy(enemyX[i], enemyY[i], i)

    #shooter movements
    if shooterY <=0:
        shooterY = 530
        shooter_state = "ready"
    if shooter_state is "fire":
        shooter(shooterX, shooterY)
        shooterY -= shooterY_change

    
    show_score(textX,textY)
    pygame.display.update()