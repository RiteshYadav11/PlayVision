import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)

# Load images
goal_post_img = pygame.image.load("GoalPost1.png")
target_img = pygame.image.load("2126746-200.png")
target_img = pygame.transform.scale(target_img, (400, 400))  # Increase size of target image

# Load sound
hit_sound = pygame.mixer.Sound("TCD25PS-game-success.mp3")

# Game loop
def main():
    # Screen dimensions
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Click the Target Game")

    # Get dimensions of images
    goal_post_rect = goal_post_img.get_rect()
    target_rect = target_img.get_rect()

    # Set margins
    top_margin = 100
    bottom_margin = 100

    # Set initial position of the target
    target_rect.center = (random.randint(width // 4, width * 3 // 4), random.randint(top_margin, height - bottom_margin))

    goal_post_img_resized = pygame.transform.scale(goal_post_img, (width, height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if target_rect.collidepoint(event.pos):
                    target_rect.center = (random.randint(width // 4, width * 3 // 4), random.randint(top_margin, height - bottom_margin))
                    hit_sound.play()  # Play sound when target is hit
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                goal_post_img_resized = pygame.transform.scale(goal_post_img, (width, height))

        # Draw everything
        screen.fill(WHITE)
        screen.blit(goal_post_img_resized, (0, 0))
        screen.blit(target_img, target_rect)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
