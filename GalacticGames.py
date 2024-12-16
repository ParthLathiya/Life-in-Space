import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Life In Space")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Font
font = pygame.font.SysFont(None, 36)

# Load astronaut image
astronaut_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\astronaut.png")
astronaut_img = pygame.transform.scale(astronaut_img, (50,70))

# Spaceship environment
spaceship_width = SCREEN_WIDTH
spaceship_height = SCREEN_HEIGHT // 2
spaceship_surface = pygame.Rect(0, SCREEN_HEIGHT // 2, spaceship_width, spaceship_height)

# Load spaceship surface image
spaceship_surface_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\spaceship_surface.png")
spaceship_width = SCREEN_WIDTH
spaceship_height = SCREEN_HEIGHT // 2
spaceship_surface_img = pygame.transform.scale(spaceship_surface_img, (spaceship_width, spaceship_height))

# Load images for food, oxygen tank, and power kit
food_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\food.png")
food_img = pygame.transform.scale(food_img, (40, 40))

oxygen_tank_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\oxygen.png")
oxygen_tank_img = pygame.transform.scale(oxygen_tank_img, (40, 40))

power_kit_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\power.png")
power_kit_img = pygame.transform.scale(power_kit_img, (40, 40))

tool_kit_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\tool.png")
tool_kit_img = pygame.transform.scale(tool_kit_img, (40, 40))

repair_kit_img = pygame.image.load("Nasa Space App 2024\\2-D Game\\repair.png")
repair_kit_img = pygame.transform.scale(repair_kit_img, (40, 40))

# Player (Astronaut) variables
astronaut_x = 100
astronaut_y = spaceship_surface.y + spaceship_surface.height - 70  # Bottom of spaceship
base_speed = 10  # Increased speed
astronaut_speed_x = 0
astronaut_speed_y = 0
friction = 0.9  # Friction factor to slow movement
acceleration = 1.5  # Acceleration factor
max_speed = 10  # Max speed to prevent too fast movement

weight = 70  # Weight in kg (starting value)
microgravity_effect = 0.005  # Weight loss factor per frame due to microgravity
health_factor = 100  # Health factor

# Health depletion thresholds
critical_oxygen_threshold = 40  # Oxygen below this level decreases health rapidly
critical_power_threshold = 30  # Power below this level decreases health
low_weight_threshold = 50  # Weight below this level decreases health due to malnutrition

# System variables (Oxygen, Power, etc.)
oxygen_level = 100  # Starting oxygen level
power_level = 100  # Starting power level
system_failure = False
system_failure_timer = 0
failure_threshold = 300  # Time until system fails completely (reduced for more urgency)

# Constants for resource depletion (starting values)
oxygen_depletion_rate = 0.075  # Constant depletion rate for oxygen
power_depletion_rate = 0.05   # Constant depletion rate for power

# Random system failure positions (random part of spaceship to repair)
system_x = random.randint(50, SCREEN_WIDTH - 100)
system_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)

# Despawn time: 7 seconds (in milliseconds)
despawn_time_ms = 7000
base_respawn_time_ms = 13000  # Base respawn time of 13 seconds (in milliseconds)

# Tool (to fix systems) variables
tools = []
num_tools = 3  # Number of tools to collect
for _ in range(num_tools):
    tool_x = random.randint(100, SCREEN_WIDTH - 100)
    tool_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
    tools.append([tool_x, tool_y, False])  # (x, y, collected)

# Food variables
food_x = random.randint(100, SCREEN_WIDTH - 100)
food_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
food_collected = False
food_spawn_time = pygame.time.get_ticks()  # Record the time when food spawns
food_despawn_time = 0  # To track when food despawns
food_respawn_time_ms = base_respawn_time_ms  # Dynamic respawn time based on difficulty

# Power Kit variables
power_kit_x = random.randint(100, SCREEN_WIDTH - 100)
power_kit_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
power_kit_collected = False
power_kit_spawn_time = pygame.time.get_ticks()  # Record the time when power kit spawns
power_kit_despawn_time = 0  # To track when power kit despawns
power_kit_respawn_time_ms = base_respawn_time_ms  # Dynamic respawn time

# Oxygen Tank variables
oxygen_tank_x = random.randint(100, SCREEN_WIDTH - 100)
oxygen_tank_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
oxygen_tank_collected = False
oxygen_tank_spawn_time = pygame.time.get_ticks()  # Record the time when oxygen tank spawns
oxygen_tank_despawn_time = 0  # To track when oxygen tank despawns
oxygen_tank_respawn_time_ms = base_respawn_time_ms  # Dynamic respawn time

# Failure handling variables
failure_timer = 0
failure_interval = random.randint(300, 800)  # Increased failure frequency
failure_penalty_timer = 0
penalty_threshold = 200  # Time after which penalty is applied (reduced)

# Game Over countdown timer
game_over_timer = 200  # Countdown timer when critical levels are low

# Difficulty management
difficulty_timer = 0  # Track how long the player has survived
difficulty_level = 1  # Start at level 1
difficulty_increase_interval = 1000  # Increase difficulty every 1000 frames
system_failure_rate_increase = 0.05  # Rate at which system failures become more frequent

# Score variable
score = 0  # Initialize score

# "How to Play" flag
show_how_to_play = False  # Track if the "How to Play" screen is displayed
show_score_instructions = False  # Track if the "Score Instructions" screen is displayed

# Clock
clock = pygame.time.Clock()

# Game Over flag
game_over = False

def draw_astronaut(x, y):
    """Draw the astronaut on the screen."""
    screen.blit(astronaut_img, (x, y))

def draw_spaceship():
    """Draw the spaceship surface using an image."""
    screen.blit(spaceship_surface_img, (0, SCREEN_HEIGHT // 2))  # Blit the spaceship image on the surface

def draw_system_failure(x, y):
    """Draw a system failure spot (where astronaut needs to go)."""
    screen.blit(repair_kit_img, (x, y))  # System failure is a red square

def draw_tool(x, y):
    """Draw the tool kit the astronaut needs to collect to fix systems."""
    screen.blit(tool_kit_img, (x, y))

def draw_food(x, y):
    """Draw the food the astronaut can collect."""
    screen.blit(food_img, (x, y))

def draw_power_kit(x, y):
    """Draw the power kit the astronaut can collect."""
    screen.blit(power_kit_img, (x, y))

def draw_oxygen_tank(x, y):
    """Draw the oxygen tank the astronaut can collect."""
    screen.blit(oxygen_tank_img, (x, y))

def show_stats():
    """Display oxygen, power levels, health factor, and score on the screen."""
    oxygen_text = font.render(f"Oxygen: {int(oxygen_level)}%", True, WHITE)
    power_text = font.render(f"Power: {int(power_level)}%", True, WHITE)
    health_factor_text = font.render(f"Health: {health_factor}%", True, WHITE)
    weight_text = font.render(f"Weight: {weight:.1f} kg", True, WHITE)
    difficulty_text = font.render(f"Difficulty: {difficulty_level}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)  # Display score
    help = font.render(f"Press 'H' for 'How to Play'", True, WHITE)
    score_ins = font.render(f"Press'S' for 'Score Instructions'", True, WHITE)
    screen.blit(oxygen_text, (10, 10))
    screen.blit(power_text, (10, 50))
    screen.blit(health_factor_text, (10, 90))
    screen.blit(weight_text, (10, 130))
    screen.blit(difficulty_text, (10, 170))
    screen.blit(help, (10, 210))
    screen.blit(score_ins, (10, 250))
    screen.blit(score_text, (325, 10))  # Place score below other stats

def draw_legend():
    """Draw a legend on the right-hand side of the screen with icons and explanations."""
    legend_x = SCREEN_WIDTH - 220
    legend_y = 20
    legend_spacing = 40

    # Legend title
    legend_title = font.render("Legend", True, WHITE)
    screen.blit(legend_title, (legend_x, legend_y))

    # Oxygen Legend
    screen.blit(oxygen_tank_img, (legend_x, legend_y + legend_spacing))
    oxygen_legend_text = font.render("Oxygen", True, WHITE)
    screen.blit(oxygen_legend_text, (legend_x + 40, legend_y + legend_spacing))

    # Power Legend
    screen.blit(power_kit_img, (legend_x, legend_y + 2 * legend_spacing))
    power_legend_text = font.render("Power", True, WHITE)
    screen.blit(power_legend_text, (legend_x + 40, legend_y + 2 * legend_spacing))

    # Tool Legend
    screen.blit(tool_kit_img, (legend_x, legend_y + 3 * legend_spacing))
    tool_legend_text = font.render("Tool", True, WHITE)
    screen.blit(tool_legend_text, (legend_x + 40, legend_y + 3 * legend_spacing))

    # Food Legend
    screen.blit(food_img, (legend_x, legend_y + 4 * legend_spacing))
    food_legend_text = font.render("Food", True, WHITE)
    screen.blit(food_legend_text, (legend_x + 40, legend_y + 4 * legend_spacing))

    # System Failure Legend
    screen.blit(repair_kit_img , (legend_x, legend_y + 5 * legend_spacing))
    system_legend_text = font.render("Repair Spot", True, WHITE)
    screen.blit(system_legend_text, (legend_x + 40, legend_y + 5 * legend_spacing))

def draw_how_to_play():
    """Draw the 'How to Play' screen."""
    screen.fill(BLACK)
    title_text = font.render("How to Play", True, WHITE)
    instruction_lines = [
        "1. Use arrow keys to move the astronaut.",
        "2. Collect food, power kits, and oxygen tanks.",
        "3. Fix system failures by collecting tools and repairing.",
        "4. Avoid running out of oxygen, power, or health.",
        "5. Press 'R' to restart if the game ends.",
        "Press 'B' to go back to the game."
    ]
    
    # Render title
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, 50))

    # Render each line of instructions
    for i, line in enumerate(instruction_lines):
        instruction_text = font.render(line, True, WHITE)
        screen.blit(instruction_text, (50, 150 + i * 40))

def draw_score_instructions():
    """Draw the 'Score Instructions' screen."""
    screen.fill(BLACK)
    title_text = font.render("Score Instructions", True, WHITE)
    score_lines = [
        "1. Collect Food: +100 points",
        "2. Collect Power Kit: +150 points",
        "3. Collect Oxygen Tank: +200 points",
        "4. Repair System: +500 points",
        "5. Failure to Repair System: -5 points per second",
        "Press 'B' to go back to the game."
    ]
    
    # Render title
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, 50))

    # Render each line of instructions
    for i, line in enumerate(score_lines):
        score_text = font.render(line, True, WHITE)
        screen.blit(score_text, (50, 150 + i * 40))

def despawn_item(spawn_time, item_collected, current_time, item_type):
    """Handle item despawn logic after 7 seconds if not collected."""
    if current_time - spawn_time > despawn_time_ms and not item_collected:
        item_collected = True  # Mark item as despawned
        print(f"{item_type} despawned!")
    return item_collected

def respawn_item(item_collected, despawn_time, current_time, respawn_type, respawn_time_ms):
    """Handle item respawn after a dynamic time of despawn."""
    if item_collected and current_time - despawn_time > respawn_time_ms:
        item_collected = False  # Respawn item
        print(f"{respawn_type} respawned!")
    return item_collected

def collect_food():
    """Handle food collection logic."""
    global food_collected, food_x, food_y, weight, health_factor, food_spawn_time, food_despawn_time, score
    food_collected = True
    food_despawn_time = pygame.time.get_ticks()  # Mark despawn time
    weight += 2  # Increase weight
    weight = min(100, weight)  # Cap weight to 100 kg
    health_factor = min(100, health_factor + 10)  # Increase health and cap it at 100%
    score += 100  # Add 100 points for collecting food

def respawn_food():
    """Respawn food after despawn."""
    global food_x, food_y, food_spawn_time
    food_x = random.randint(100, SCREEN_WIDTH - 100)  # Respawn at random position
    food_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
    food_spawn_time = pygame.time.get_ticks()  # Reset spawn time

def collect_oxygen_tank():
    """Handle oxygen tank collection logic."""
    global oxygen_tank_collected, oxygen_tank_x, oxygen_tank_y, oxygen_level, oxygen_tank_spawn_time, oxygen_tank_despawn_time, score
    oxygen_tank_collected = True
    oxygen_tank_despawn_time = pygame.time.get_ticks()  # Mark despawn time
    oxygen_level = min(100, oxygen_level + 30)  # Increase oxygen level and cap it at 100%
    score += 200  # Add 200 points for collecting oxygen tank

def respawn_oxygen_tank():
    """Respawn oxygen tank after despawn."""
    global oxygen_tank_x, oxygen_tank_y, oxygen_tank_spawn_time
    oxygen_tank_x = random.randint(100, SCREEN_WIDTH - 100)  # Respawn at random position
    oxygen_tank_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
    oxygen_tank_spawn_time = pygame.time.get_ticks()  # Reset spawn time

def collect_power_kit():
    """Handle power kit collection logic."""
    global power_kit_collected, power_kit_x, power_kit_y, power_level, power_kit_spawn_time, power_kit_despawn_time, score
    power_kit_collected = True
    power_kit_despawn_time = pygame.time.get_ticks()  # Mark despawn time
    power_level = min(100, power_level + 20)  # Increase power level and cap it at 100%
    score += 150  # Add 150 points for collecting power kit

def respawn_power_kit():
    """Respawn power kit after despawn."""
    global power_kit_x, power_kit_y, power_kit_spawn_time
    power_kit_x = random.randint(100, SCREEN_WIDTH - 100)  # Respawn at random position
    power_kit_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
    power_kit_spawn_time = pygame.time.get_ticks()  # Reset spawn time

def all_tools_collected():
    """Check if all tools have been collected."""
    return all(tool[2] for tool in tools)

def repair_system():
    """Repair the system failure if the astronaut is near it and has all tools."""
    global system_failure, oxygen_level, power_level, system_x, system_y, score
    
    # Check if astronaut is near the failure and has all tools
    if (astronaut_x < system_x + 60 and astronaut_x + 50 > system_x and
        astronaut_y < system_y + 60 and astronaut_y + 70 > system_y and
        all_tools_collected()):
        system_failure = False  # System is repaired
        system_x = random.randint(50, SCREEN_WIDTH - 100)  # Move failure to a new random position
        system_y = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
        oxygen_level = min(100, oxygen_level + 20)  # Restore oxygen and cap it at 100%
        power_level = min(100, power_level + 20)  # Restore power and cap it at 100%
        score += 500  # Add 500 points for repairing system
        respawn_tools()  # Respawn tools after repair

def respawn_tools():
    """Respawn tools in new random positions after each repair."""
    for tool in tools:
        tool[0] = random.randint(100, SCREEN_WIDTH - 100)
        tool[1] = random.randint(spaceship_surface.y + 50, spaceship_surface.y + spaceship_surface.height - 100)
        tool[2] = False  # Mark the tools as not collected

def reset_game():
    """Reset game variables for a new game."""
    global astronaut_x, astronaut_y, oxygen_level, power_level, system_failure, weight, health_factor, game_over_timer, difficulty_level, failure_interval, score
    astronaut_x = 100
    astronaut_y = spaceship_surface.y + spaceship_surface.height - 70
    oxygen_level = 100
    power_level = 100
    system_failure = False
    weight = 70
    health_factor = 100
    game_over_timer = 200  # Reset game over countdown timer
    difficulty_level = 1  # Reset difficulty
    failure_interval = random.randint(300, 800)  # Reset system failure rate
    score = 0  # Reset score
    respawn_tools()

# Define the missing `increase_difficulty` function
def increase_difficulty():
    """Increase the difficulty of the game over time."""
    global oxygen_depletion_rate, power_depletion_rate, difficulty_level, failure_interval
    global food_respawn_time_ms, power_kit_respawn_time_ms, oxygen_tank_respawn_time_ms

    # Increase depletion rates and failure rate
    oxygen_depletion_rate += 0.01  # Oxygen depletes faster
    power_depletion_rate += 0.01  # Power depletes faster
    difficulty_level += 1  # Increase difficulty level

    # Make system failures occur more frequently
    failure_interval = max(200, failure_interval - 50)  # Reduce interval, but not below 200 ms

    # Decrease respawn times based on increased difficulty (make items respawn faster)
    food_respawn_time_ms = max(4000, base_respawn_time_ms - (difficulty_level * 500))
    power_kit_respawn_time_ms = max(4000, base_respawn_time_ms - (difficulty_level * 500))
    oxygen_tank_respawn_time_ms = max(4000, base_respawn_time_ms - (difficulty_level * 500))

    print(f"Difficulty increased to level {difficulty_level}! Oxygen/power depletion rates increased.")
# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for toggling between screens
    keys = pygame.key.get_pressed()
    if keys[pygame.K_h]:
        show_how_to_play = True  # Show the "How to Play" screen
    if keys[pygame.K_b]:
        show_how_to_play = False  # Go back to the game
        show_score_instructions = False  # Go back from score instructions
    if keys[pygame.K_s]:
        show_score_instructions = True  # Show the score instructions screen

    if show_how_to_play:
        draw_how_to_play()  # Draw the "How to Play" screen
    elif show_score_instructions:
        draw_score_instructions()  # Draw the "Score Instructions" screen
    else:
        # Existing game logic here (main game loop)
        screen.fill(BLACK)

        if not game_over:
            # Handle controls
            if keys[pygame.K_LEFT]:
                astronaut_speed_x -= acceleration
            if keys[pygame.K_RIGHT]:
                astronaut_speed_x += acceleration
            if keys[pygame.K_UP]:
                astronaut_speed_y -= acceleration
            if keys[pygame.K_DOWN]:
                astronaut_speed_y += acceleration

            # Apply friction to slow down movement
            astronaut_speed_x *= friction
            astronaut_speed_y *= friction

            # Cap speed to max_speed
            astronaut_speed_x = max(-max_speed, min(max_speed, astronaut_speed_x))
            astronaut_speed_y = max(-max_speed, min(max_speed, astronaut_speed_y))

            # Update astronaut's position
            astronaut_x += astronaut_speed_x
            astronaut_y += astronaut_speed_y

            # Keep astronaut within spaceship bounds
            astronaut_x = max(0, min(SCREEN_WIDTH - 50, astronaut_x))
            astronaut_y = max(spaceship_surface.y + 10, min(spaceship_surface.y + spaceship_surface.height - 70, astronaut_y))

            # Constant depletion of oxygen and power levels
            oxygen_level -= oxygen_depletion_rate  # Constant depletion rate for oxygen
            power_level -= power_depletion_rate    # Constant depletion rate for power

            # Gradually decrease weight due to microgravity
            weight -= microgravity_effect
            if weight < low_weight_threshold:
                health_factor -= 0.05  # Gradual health reduction if weight drops too low

            # **Impact on health based on oxygen levels**
            if oxygen_level < critical_oxygen_threshold:
                health_factor -= 0.1  # Health decreases faster when oxygen is low

            # **Impact on health based on power levels**
            if power_level < critical_power_threshold:
                health_factor -= 0.05  # Health decreases if power is low

            # Cap all vital parameters at 100%
            oxygen_level = min(100, oxygen_level)
            power_level = min(100, power_level)
            health_factor = min(100, health_factor)

            # Get current time
            current_time = pygame.time.get_ticks()
            
             # Despawn items after 7 seconds if not collected
            food_collected = despawn_item(food_spawn_time, food_collected, current_time, "Food")
            power_kit_collected = despawn_item(power_kit_spawn_time, power_kit_collected, current_time, "Power Kit")
            oxygen_tank_collected = despawn_item(oxygen_tank_spawn_time, oxygen_tank_collected, current_time, "Oxygen Tank")

            # Respawn items after dynamic time of despawn
            if food_collected:
                if current_time - food_despawn_time > food_respawn_time_ms:
                    respawn_food()  # Respawn food at a new location
                    food_collected = False

            if power_kit_collected:
                if current_time - power_kit_despawn_time > power_kit_respawn_time_ms:
                    respawn_power_kit()  # Respawn power kit
                    power_kit_collected = False

            if oxygen_tank_collected:
                if current_time - oxygen_tank_despawn_time > oxygen_tank_respawn_time_ms:
                    respawn_oxygen_tank()  # Respawn oxygen tank
                    oxygen_tank_collected = False

            # Update failure timer
            if not system_failure:
                failure_timer += 1

                # Trigger system failure at a random time
                if failure_timer >= failure_interval:
                    system_failure = True
                    failure_timer = 0  # Reset the timer
                    failure_interval = random.randint(300, 800)  # Set a new random interval

            # Apply penalty if system failure is not repaired in time
            if system_failure:
                failure_penalty_timer += 1
                if failure_penalty_timer >= penalty_threshold:
                    oxygen_level -= 0.1  # Deplete oxygen faster
                    power_level -= 0.1  # Deplete power faster
                    score -= 5  # Deduct 5 points for failing to repair the system in time

            # Reset penalty timer when system is repaired
            if not system_failure:
                failure_penalty_timer = 0

            # Repair system if conditions are met
            if system_failure:
                repair_system()

            # Increase difficulty over time
            difficulty_timer += 1
            if difficulty_timer >= difficulty_increase_interval:
                increase_difficulty()  # Call the function to increase difficulty
                difficulty_timer = 0

            # Collect food
            if (astronaut_x < food_x + 20 and astronaut_x + 50 > food_x and
                astronaut_y < food_y + 20 and astronaut_y + 70 > food_y and not food_collected):
                collect_food()

            # Collect power kit
            if (astronaut_x < power_kit_x + 25 and astronaut_x + 50 > power_kit_x and
                astronaut_y < power_kit_y + 25 and astronaut_y + 70 > power_kit_y and not power_kit_collected):
                collect_power_kit()

            # Collect oxygen tank
            if (astronaut_x < oxygen_tank_x + 25 and astronaut_x + 50 > oxygen_tank_x and
                astronaut_y < oxygen_tank_y + 25 and astronaut_y + 70 > oxygen_tank_y and not oxygen_tank_collected):
                collect_oxygen_tank()

            # Collect tools
            for tool in tools:
                if (astronaut_x < tool[0] + 30 and astronaut_x + 50 > tool[0] and
                    astronaut_y < tool[1] + 30 and astronaut_y + 70 > tool[1]):
                    tool[2] = True  # Mark tool as collected

            # Check for game over conditions
            if oxygen_level <= 0 or power_level <= 0 or health_factor <= 0:
                game_over = True

            # Draw everything
            draw_spaceship()
            draw_astronaut(astronaut_x, astronaut_y)
            for tool in tools:
                if not tool[2]:
                    draw_tool(tool[0], tool[1])
            if not food_collected:
                draw_food(food_x, food_y)
            if not power_kit_collected:
                draw_power_kit(power_kit_x, power_kit_y)
            if not oxygen_tank_collected:
                draw_oxygen_tank(oxygen_tank_x, oxygen_tank_y)
            if system_failure:
                draw_system_failure(system_x, system_y)
            show_stats()
            draw_legend()  # Draw the legend on the right-hand side

        else:
            # Display Game Over message
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            
            # Display the final score
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

            # Display restart instruction
            press_key_text = font.render("Press R to restart", True, WHITE)
            screen.blit(press_key_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
