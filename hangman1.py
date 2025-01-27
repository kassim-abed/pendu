import pygame
import random

# Function to read words from a text file
def read_words(file):
    try:
        with open(file, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return ['PYTHON', 'PYGAME', 'HANGMAN', 'GAME', 'CODE']

# Function to add a word to the text file
def add_word(file, word):
    with open(file, 'a') as f:
        f.write(f'\n{word}')

# Function to draw the hangman based on remaining attempts
def draw_hangman(surface, attempts):
    if attempts <= 7:  # Structure of the hangman
        pygame.draw.line(surface, black, (50, 500), (50, 100), 5)  # Vertical bar
        pygame.draw.line(surface, black, (50, 100), (200, 100), 5)  # Top bar
        pygame.draw.line(surface, black, (200, 100), (200, 150), 5)  # Rope
    if attempts <= 6: pygame.draw.circle(surface, black, (200, 200), 50, 5)  # Head
    if attempts <= 5: pygame.draw.line(surface, black, (200, 250), (200, 400), 5)  # Body
    if attempts <= 4: pygame.draw.line(surface, black, (200, 300), (150, 350), 5)  # Left arm
    if attempts <= 3: pygame.draw.line(surface, black, (200, 300), (250, 350), 5)  # Right arm
    if attempts <= 2: pygame.draw.line(surface, black, (200, 400), (150, 450), 5)  # Left leg
    if attempts <= 1: pygame.draw.line(surface, black, (200, 400), (250, 450), 5)  # Right leg

# Initialize Pygame
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hangman Game')

# Colors
white, black = (255, 255, 255), (0, 0, 0)

# Fonts
font, button_font = pygame.font.Font(None, 74), pygame.font.Font(None, 36)

# Button class for creating buttons
class Button:
    def __init__(self, text, x, y, action=None):
        self.text = text
        self.rect = pygame.Rect(x - 50, y, 100, 50)
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, black, self.rect, 2)
        text_surface = button_font.render(self.text, True, black)
        surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def check_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.action:
            self.action()

# Game functions
def play_game():
    global game_active, secret_word, found_letters, remaining_attempts, used_letters, game_over, message
    game_active = True
    game_over = False
    message = ""
    secret_word = random.choice(words)
    found_letters = ['_'] * len(secret_word)
    remaining_attempts = 7
    used_letters = []

def add_words():
    global adding_words
    adding_words = True

def quit_game():
    global running
    running = False

def return_to_menu():
    global game_active, adding_words, game_over, secret_word, found_letters, remaining_attempts, used_letters, message
    game_active = False
    adding_words = False
    game_over = False
    secret_word = ""
    found_letters = []
    remaining_attempts = 7
    used_letters = []
    message = ""

def draw_input_box():
    input_box = pygame.Rect(width // 2 - 150, height // 2 + 100, 300, 50)
    pygame.draw.rect(window, black, input_box, 2)
    window.blit(button_font.render(new_word, True, black), (input_box.x + 5, input_box.y + 10))

def display_message(message, y_offset=0):
    text_surface = button_font.render(message, True, black)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    window.blit(text_surface, text_rect)

# Create buttons
buttons = [
    Button("Play", width // 2 - 50, height // 2 - 150, play_game),
    Button("Add Words", width // 2 - 50, height // 2 - 50, add_words),
    Button("Quit", width // 2 - 50, height // 2 + 50, quit_game),
]

# Create the return button
return_button = Button("Return", width - 150, 50, return_to_menu)

# Read words from the text file
words = read_words('words.txt')
game_active = adding_words = game_over = False
new_word, secret_word = "", ""
found_letters, remaining_attempts = [], 0
used_letters = []
message = ""
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_active and not game_over:
                letter = event.unicode.upper()
                if letter in secret_word and letter not in used_letters:
                    used_letters.append(letter)
                    for i, l in enumerate(secret_word):
                        if l == letter:
                            found_letters[i] = letter
                    if '_' not in found_letters:
                        game_over = True
                        message = "Congratulations! You won!"
                        display_message(message, 50)
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        return_to_menu()
                elif letter not in secret_word and letter not in used_letters:
                    remaining_attempts -= 1
                    used_letters.append(letter)
                    if remaining_attempts <= 0:
                        game_over = True
                        message = f"You lost! The word was: {secret_word}"
                        display_message(message, 50)
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        return_to_menu()
            elif adding_words:
                if event.key == pygame.K_RETURN:
                    add_word('words.txt', new_word.upper())
                    words.append(new_word.upper())
                    new_word, adding_words = "", False
                elif event.key == pygame.K_BACKSPACE:
                    new_word = new_word[:-1]
                else:
                    new_word += event.unicode.upper()

    window.fill(white)

    if game_active:
        window.blit(font.render(' '.join(found_letters), True, black), (width // 2 - 150, height // 2 - 37))
        window.blit(font.render(f"Remaining attempts: {remaining_attempts}", True, black), (width // 2 - 200, height - 100))
        window.blit(button_font.render(f"Used letters: {', '.join(used_letters)}", True, black), (width // 2 - 200, height - 150))
        draw_hangman(window, remaining_attempts)
    elif adding_words:
        draw_input_box()
    else:
        for button in buttons:
            button.draw(window)
            button.check_click()
        if message:
            display_message(message, 50)

    pygame.display.flip()

pygame.quit()
