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

# Global variables
# answer = None
start_time = pygame.time.get_ticks()  # Start time for the timer
timer_font = pygame.font.Font(None, 36)

# Function to generate a question
def generate_question():
    global answer
    # num1 = random.randint(1, 10)
    # num2 = random.randint(1, 5)
    num1 = 4
    num2 = 2
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    elif operation == '*':
        answer = num1 * num2
    else:
        answer = num1 // num2
    question_text = f"{num1} {operation} {num2} = ?"
    return question_text, answer

# Load balloon images
original_balloon_images = [pygame.image.load(f'Balloons/Balloon{i}.png') for i in range(1, 5)]
balloon_images = [pygame.transform.scale(img, (200, 250)) for img in original_balloon_images]  # Resize to 100x100
balloon_width, balloon_height = 200, 250  # Adjusted size

# Function to reset the balloon
def resetBalloon():
    global x, y, balloon_number
    x = random.randint(0, gameDisplay.get_width() - balloon_width)
    y = gameDisplay.get_height()
    balloon_number = random.randint(1, len(balloon_images))  # Assign a random balloon number

# Function to generate and display a new question
def generate_and_display_question():
    global question_text
    question_text, answer = generate_question()  # Generate a new question
    display_question(question_text)

# Function to display the question at the top of the game window
def display_question(question_text):
    text = font.render(question_text, True, black)
    text_rect = text.get_rect(center=(display_width // 2, 50))
    gameDisplay.blit(text, text_rect)

# Function to display the score
def display_score(score):
    text = font.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, (10, 10))  # Display score below the question

# Function to draw the balloon
def car(x, y):
    gameDisplay.blit(balloon_images[balloon_number - 1], (x, y))  # Draw the current balloon image

score = 0
# resetBalloon()

stored_value = 0  # Variable to store the accumulated value

# Generate and display the initial question
generate_and_display_question()
resetBalloon()

# Main game loop
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if x <= mouseX <= x + balloon_width and y <= mouseY <= y + balloon_height:
                stored_value += balloon_number  # Accumulate the clicked balloon number
                print("Clicked balloon with number:", balloon_number, "Stored value:", stored_value)
                # Check if the stored value matches the answer
                resetBalloon()
                if stored_value == answer:
                    score += 1
                    print("Correct answer!")
                    generate_and_display_question()  # Generate and display a new question
                    resetBalloon()  # Reset the balloon position
                    stored_value = 0
                elif stored_value > answer:
                    print("Stored value exceeds the answer. Resetting...")
                    stored_value = 0
        elif event.type == pygame.VIDEORESIZE:
            display_width, display_height = event.size
            gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
            resetBalloon()

    gameDisplay.fill(white)
    display_question(question_text)  # Display the question text before drawing the balloon
    car(x, y)
    y -= balloon_speed

    if y < -balloon_height:
        resetBalloon()

    display_score(score)
    
    # Calculate and display timer
    current_time = pygame.time.get_ticks() - start_time
    timer_text = timer_font.render("Time: " + str(current_time // 1000), True, black)
    gameDisplay.blit(timer_text, (display_width - 150, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
