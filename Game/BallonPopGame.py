import pygame
import random

pygame.init()

display_width = 800
display_height = 600
balloon_speed = 2

gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption('Balloon Game')

black = (0, 0, 0)
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('Ballon1.png')
balloon_width, balloon_height = 800, 800  # Initial size, can be adjusted

def resetBalloon():
    global x, y
    x = random.randint(0, gameDisplay.get_width() - balloon_width)
    y = gameDisplay.get_height()

def display_score(score):
    text = font.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, (10, 10)) 

def car(x, y):
    gameDisplay.blit(carImg, (x, y))

score = 0
resetBalloon()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if x <= mouseX <= x + balloon_width and y <= mouseY <= y + balloon_height:
                score += 1
                resetBalloon()
        elif event.type == pygame.VIDEORESIZE:
            display_width, display_height = event.size
            gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
            resetBalloon()

    gameDisplay.fill(white)
    car(x, y)
    y -= balloon_speed

    if y < -balloon_height:
        resetBalloon()

    display_score(score)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

