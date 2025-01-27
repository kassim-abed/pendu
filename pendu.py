import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 30)

fichier_mots = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mots.txt')

def draw_text(text, x, y, font, color):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def add_word():
    running = True
    word = ""
    feedback_message = ""
    message_display_time = 2000  # Temps d'affichage du message (en millisecondes)
    timer_started = False
    start_time = 0

    while running:
        screen.fill(WHITE)
        draw_text("Enter a word to add:", 200, 200, font, BLACK)
        draw_text("Press Enter to save or ESC to cancel", 200, 300, small_font, BLACK)
        draw_text(word, 200, 400, font, BLACK)
        draw_text(feedback_message, 200, 450, small_font, GREEN)
        pygame.display.update()

        current_time = pygame.time.get_ticks()  # Temps actuel en millisecondes

        if timer_started and current_time - start_time > message_display_time:
            running = False  # Quitter l'ajout après quelques secondes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Ajouter le mot
                    if word.isalpha():
                        with open(fichier_mots, 'a') as file:
                            file.write(f" {word}")
                        feedback_message = f"Word '{word}' added!"
                        word = ""
                        timer_started = True  # Démarrer le timer après un ajout réussi
                        start_time = current_time
                    else:
                        feedback_message = "Invalid word! Use letters only."
                        timer_started = True  # Démarrer le timer après une erreur
                        start_time = current_time
                elif event.key == pygame.K_ESCAPE:  # Quitter manuellement
                    running = False
                elif event.key == pygame.K_BACKSPACE:  # Effacer le dernier caractère
                    word = word[:-1]
                else:
                    letter = pygame.key.name(event.key)
                    if letter.isalpha():
                        word += letter.lower()


            screen.fill(WHITE)
            draw_text("Enter a word to add:", 200, 200, font, BLACK)
            draw_text("Press Enter to save or ESC to cancel", 200, 300, small_font, BLACK)
            draw_text(word, 200, 400, font, BLACK)
            pygame.display.update()

def play():
    with open(fichier_mots, 'r') as file:
        allText = file.read()
        word_to_guess = random.choice(list(map(str, allText.split())))

    guessed_word = ['_'] * len(word_to_guess)
    incorrect_guesses = []
    max_attempts = 6
    attempts_left = max_attempts

    def draw_hangman(attempts_left):
        if attempts_left <= 5:
            pygame.draw.circle(screen, BLACK, (650, 320), 25, 5)
        if attempts_left <= 4:
            pygame.draw.line(screen, BLACK, (650, 340), (650, 450), 5)
        if attempts_left <= 3:
            pygame.draw.line(screen, BLACK, (650, 350), (630, 430), 5)
        if attempts_left <= 2:
            pygame.draw.line(screen, BLACK, (650, 350), (670, 430), 5)
        if attempts_left <= 1:
            pygame.draw.line(screen, BLACK, (650, 450), (630, 530), 5)
        if attempts_left <= 0:
            pygame.draw.line(screen, BLACK, (650, 450), (670, 530), 5)

    running = True
    while running:
        screen.fill(WHITE)

        pygame.draw.line(screen, BLACK, (500, 250), (500, 550), 5)
        pygame.draw.line(screen, BLACK, (425, 550), (575, 550), 5)
        pygame.draw.line(screen, BLACK, (500, 250), (650, 250), 5)
        pygame.draw.line(screen, BLACK, (650, 250), (650, 300), 5)
        pygame.draw.line(screen, BLACK, (500, 250), (550, 250), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key).lower()
                if guess.isalpha() and guess not in incorrect_guesses and guess not in guessed_word:
                    if guess in word_to_guess:
                        for i in range(len(word_to_guess)):
                            if word_to_guess[i] == guess:
                                guessed_word[i] = guess
                    else:
                        incorrect_guesses.append(guess)
                        attempts_left -= 1

        draw_text("Word to guess: " + " ".join(guessed_word), 50, 50, font, BLACK)
        draw_text("Incorrect letters: " + ", ".join(incorrect_guesses), 50, 100, small_font, BLACK)
        draw_text(f"Attempts remaining: {attempts_left}", 50, 150, small_font, BLACK)

        draw_hangman(attempts_left)

        if "".join(guessed_word) == word_to_guess:
            draw_text("You won! The word was: " + word_to_guess, 50, 200, font, GREEN)
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

        if attempts_left == 0:
            draw_text(f"You lost! The word was: {word_to_guess}", 50, 200, font, RED)
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

        pygame.display.update()

def main_hub():
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Welcome to Hangman!", 250, 100, font, BLACK)
        draw_text("Press 1 to Play", 300, 200, small_font, BLACK)
        draw_text("Press 2 to Add a Word", 300, 250, small_font, BLACK)
        draw_text("Press Q to Quit", 300, 300, small_font, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play()
                elif event.key == pygame.K_2:
                    add_word()
                elif event.key == pygame.K_q:
                    running = False

        pygame.display.update()

    pygame.quit()

main_hub()
