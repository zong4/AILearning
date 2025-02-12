import random
import pygame
import math

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Define the pay - off matrix for the Prisoner's Dilemma
PAYOFF_MATRIX = {
    ('cooperate', 'cooperate'): (3, 3),
    ('cooperate', 'defect'): (-3, 3),
    ('defect', 'cooperate'): (3, -3),
    ('defect', 'defect'): (-3, -3)
}

# Define different strategies
def always_cooperate(history):
    return 'cooperate'

def always_defect(history):
    return 'defect'

def tit_for_tat(history):
    if not history:
        return 'cooperate'
    return history[-1][1]

def random_choice(history):
    return random.choice(['cooperate', 'defect'])

# Player class
class Player:
    def __init__(self, strategy, score):
        self.strategy = strategy
        self.score = score
        self.history = []

    def make_choice(self):
        return self.strategy(self.history)

    def update_score(self, payoff):
        self.score += payoff

    def update_history(self, own_choice, other_choice):
        self.history.append((own_choice, other_choice))

# Function to play a round of Prisoner's Dilemma between two players
def play_round(player1, player2):
    choice1 = player1.make_choice()
    choice2 = player2.make_choice()

    payoff1, payoff2 = PAYOFF_MATRIX[(choice1, choice2)]

    player1.update_score(payoff1)
    player2.update_score(payoff2)

    player1.update_history(choice1, choice2)
    player2.update_history(choice2, choice1)

# Function to get position on the circle
def get_position_on_circle(center_x, center_y, radius, angle):
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    return x, y

# Function to run the simulation
def run_simulation(strategies, num_players_per_strategy, start_score):
    players = []

    # Create players with equal distribution of strategies
    for strategy in strategies:
        for _ in range(num_players_per_strategy):
            players.append(Player(strategy, start_score))
    random.shuffle(players)
    players_drawing = players.copy()

    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Prisoner's Dilemma Simulation")
    font = pygame.font.Font(None, 24)

    clock = pygame.time.Clock()

    center_x = screen_width // 2
    center_y = screen_height // 2
    circle_radius = 200
    square_size = 20

    # Pause/Resume button setup
    button_width = 100
    button_height = 50
    button_x = screen_width - button_width - 20
    button_y = 20
    paused = False

    original_positions = []
    num_original_players = len(players)
    for i in range(num_original_players):
        angle = 2 * math.pi * i / num_original_players
        x, y = get_position_on_circle(center_x, center_y, circle_radius, angle)
        original_positions.append((x - square_size // 2, y - square_size // 2))

    round_num = 0
    while True:
        if not paused:
            for i in range(0, len(players)):
                play_round(players[i], players[(i + 1) % len(players)])
            players = [player for player in players if player.score > 0]

            round_num += 1
            # paused = True

        screen.fill(WHITE)

        # Draw the circle
        pygame.draw.circle(screen, BLACK, (center_x, center_y), circle_radius, 2)

        for i in range(num_original_players):
            player = players_drawing[i]
            x, y = original_positions[i]

            if(player.score < 0):
                continue

            if player.strategy == always_cooperate:
                color = GREEN
            elif player.strategy == always_defect:
                color = RED
            elif player.strategy == tit_for_tat:
                color = BLUE
            elif player.strategy == random_choice:
                color = YELLOW

            pygame.draw.rect(screen, color, (x, y, square_size, square_size))

            score_text = font.render(str(player.score), True, BLACK)
            screen.blit(score_text, (x + square_size // 2 - score_text.get_width() // 2,
                                        y + square_size // 2 - score_text.get_height() // 2))

        # Draw Pause/Resume button
        button_text = "Pause" if not paused else "Resume"
        button_surface = font.render(button_text, True, BLACK)
        pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
        screen.blit(button_surface, (button_x + button_width // 2 - button_surface.get_width() // 2,
                                     button_y + button_height // 2 - button_surface.get_height() // 2))

        # Display round number
        round_text = font.render(f"Round: {round_num}", True, BLACK)
        screen.blit(round_text, (20, 20))

        # Display color - strategy legend in the top - left corner
        legend_y = 60
        legend_texts = [
            (GREEN, "Always Cooperate"),
            (RED, "Always Defect"),
            (BLUE, "Tit for Tat"),
            (YELLOW, "Random Choice"),
        ]
        
        for color, text in legend_texts:
            pygame.draw.rect(screen, color, (20, legend_y, 20, 20))
            legend_text = font.render(text, True, BLACK)
            screen.blit(legend_text, (50, legend_y))
            legend_y += 30

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (button_x <= mouse_x <= button_x + button_width and
                        button_y <= mouse_y <= button_y + button_height):
                    paused = not paused

        # Control the update speed per round
        clock.tick(1)

# Run the simulation
strategies = [always_cooperate, always_defect, tit_for_tat, random_choice]
run_simulation(strategies, num_players_per_strategy=10, start_score=9)