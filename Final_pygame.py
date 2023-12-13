import pygame
import os
import random
from pygame.locals import *
 
# Initialize Pygame
pygame.init()
 
# Constants
WIDTH, HEIGHT = 1000, 700
FPS = 30
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)
BROWN = (139, 69, 19)
 
# Load the image for the top left corner
top_left_image = pygame.image.load("C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project\\logo.png")
top_left_image = pygame.transform.scale(top_left_image, (150, 50))
 
# Set up the timer
total_time = 90  # in seconds
current_time = total_time
clock = pygame.time.Clock()
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)
current_player = "Player"
 
# Flag to check if the player clicked the Play button
play_button_clicked = False
 
def freeze_panel():
    pygame.mouse.set_visible(False)  # Hide the mouse cursor
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)  # Block mouse button events
    pygame.event.set_blocked(pygame.MOUSEMOTION)  # Block mouse motion events
 
def unfreeze_panel():
    pygame.mouse.set_visible(True)  # Show the mouse cursor
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)  # Allow mouse button events
    pygame.event.set_allowed(pygame.MOUSEMOTION)  # Allow mouse motion events
 
# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rummikub")
 
# Load background image
background_image = pygame.image.load("C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project\\wood.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
 
# Define button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
 
SAT_BUTTON_WIDTH, SAT_BUTTON_HEIGHT = 180, 50
 
# Create Rect objects for buttons
play_button_rect = pygame.Rect(100, 575, BUTTON_WIDTH, BUTTON_HEIGHT)
group_button_rect = pygame.Rect(250, 575, BUTTON_WIDTH, BUTTON_HEIGHT)
run_button_rect = pygame.Rect(400, 575, BUTTON_WIDTH, BUTTON_HEIGHT)
pool_button_rect = pygame.Rect(550, 575, BUTTON_WIDTH, BUTTON_HEIGHT)
show_all_tiles_rect = pygame.Rect(700, 575, SAT_BUTTON_WIDTH, SAT_BUTTON_HEIGHT)
#ct_button_rect = pygame.Rect(250, 640, BUTTON_WIDTH, BUTTON_HEIGHT) # Define game board dimensions
play_for_me_button_rect = pygame.Rect(700, 640, 150, BUTTON_HEIGHT)
 
 
global player_score
player_score = 0

global comp_score
comp_score = 0
 
# Define game board dimensions
BOARD_WIDTH, BOARD_HEIGHT = 800, 300
 
# Create Rect object for the game board
game_board_rect = pygame.Rect(100, 175, BOARD_WIDTH, BOARD_HEIGHT)
 
# Create Rect objects for player's and computer's racks
player_rack_rect = pygame.Rect(100, 100, BOARD_WIDTH, 60)
computer_rack_rect = pygame.Rect(100, 500, BOARD_WIDTH, 60)
 
# Adding and Loading the Images
base_path_1 = "C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project\\images\\"
base_path_2 = "C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project\\images-1\\"
colors = ["blue", "yellow", "red", "orange", "green"]
 
image_paths_1 = [f"{base_path_1}tile_{i}_{color}.png" for color in colors for i in range(1, 16)]
image_paths_2 = [f"{base_path_2}tile_{i}_{color}.png" for color in colors for i in range(1, 16)]
 
# Shuffle the image paths to get random sets
random.shuffle(image_paths_1)
random.shuffle(image_paths_2)
 
def is_valid_group_or_run(tile_numbers):
    # Check if it's a run
    if all(num % 2 == tile_numbers[0] % 2 for num in tile_numbers):
        return True
    # Check if it's a group
    if len(set(tile_numbers)) == 1:
        return True
    return False
 
# Function to select a random set of tiles that form a valid group or run
def select_valid_group_or_run(image_paths, num_tiles):
    while True:
        selected_tiles = random.sample(image_paths, num_tiles)
        tile_numbers = [int(tile.split('_')[1]) for tile in selected_tiles]
        if is_valid_group_or_run(tile_numbers):
            return selected_tiles
 
# Select 15 random images for the player's rack with valid groups or runs
player_rack_images = select_valid_group_or_run(image_paths_1, 8) + select_valid_group_or_run(image_paths_2, 7)
# Select 15 random images for the computer's rack with valid groups or runs
computer_rack_images = select_valid_group_or_run(image_paths_1, 8) + select_valid_group_or_run(image_paths_2, 7)
 
# Combine the rest of the images for the pool
pool_images = image_paths_1 + image_paths_2
 
# Remove the tiles used in player and computer racks from the pool
pool_images = [tile for tile in pool_images if tile not in player_rack_images + computer_rack_images]
 
# Trim pool_images to a maximum length of 120
pool_images = pool_images[:120]
 
# Optionally, shuffle the pool_images if needed
random.shuffle(pool_images)
 
# Load images
player_images = [pygame.image.load(os.path.join("C:\\path_to_images", path)) for path in player_rack_images]
computer_images = [pygame.image.load(os.path.join("C:\\path_to_images", path)) for path in computer_rack_images]
pool_rack_images = [pygame.image.load(os.path.join("C:\\path_to_images", path)) for path in pool_images]
 
# Font for text boxes
font = pygame.font.Font(None, 24)
italic_font = pygame.font.SysFont("italic", 24, italic=True)
heading_font = pygame.font.SysFont("italic", 56, italic=True)
 
# Load a custom font file (replace 'your_font_file.ttf' with the actual path to your font file)
custom_font = pygame.font.Font("AbrilFatface-Regular.ttf", 36)
 
# Game loop
running = True
clock = pygame.time.Clock()
remaining_deck_images = pool_rack_images.copy()
 
# Variables for dragging
dragging = False
selected_image = None
selected_index = None
original_position = None
dragged_image_rect = None
 
# Variables for dragging on the game board
game_board_dragging = False
game_board_selected_index = None
 
# Variables for horizontal scrolling
scroll_offset_player = 0
scroll_offset_computer = 0
 
spacing = 10
 
game_board_tiles = []
comp_board_tiles = []
 
 
# ---------------- GROUPS AND RUNS LIST ---------------------
groups_and_runs_mini_list = []
groups_and_runs_main_list = []
 
# Initialize a list to store mini lists
mini_lists = []
current_mini_list = []
only_tile_name = []
 
# Variable to track whether to show computer rack images
show_computer_rack = False
 
# -------------------GRID LOGIC----------------------
 
# Assuming each image in player_images has the same width and height
cell_width = player_images[0].get_width() + 2
cell_height = player_images[0].get_height()
 
# Stroke color for the grid
grid_stroke_color = (255, 255, 255)
 
# Calculate the number of rows and columns based on the BOARD_WIDTH and BOARD_HEIGHT
num_rows = BOARD_HEIGHT // cell_height
num_columns = BOARD_WIDTH // cell_width
 
# Create a 2D grid of rectangles with stroke rectangles
game_board_grid = [[{
    'cell_rect': pygame.Rect(
        100 + col * cell_width, 175 + row * cell_height, cell_width, cell_height
    ),
    'stroke_rect': pygame.Rect(
        100 + col * cell_width, 175 + row * cell_height, cell_width, cell_height
    ),
    'image_path': None  # Initially, no image assigned
} for col in range(num_columns)] for row in range(num_rows)]
 
# Initialize a list to store occupied cell coordinates
occupied_cells = []
 
# Function to check if a cell is empty
def is_cell_empty(row, col):
    return (row, col) not in occupied_cells
 
game_board_grid_tl = pygame.Rect(game_board_grid[0][0]['cell_rect']).topleft
 
 
# ----------------------- GRID LOGIC ENDS ------------------------
 
def draw_cards_from_pool():
    # Draw two random cards from the pool
    drawn_cards = random.sample(pool_images, 2)
    # Display a prompt to select one card
    selected_card_index = None
    selected_image = None
    while selected_card_index not in [0, 1]:
        # Render the prompt
        # Render the prompt background
 
        prompt_text = font.render("Select a card:", True, (0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
 
        prompt_background = pygame.Surface((prompt_rect.width, prompt_rect.height))
        prompt_background.fill((255, 255, 255))
 
        screen.blit(prompt_background, prompt_rect.topleft)
        screen.blit(prompt_text, prompt_rect.topleft)
        # Render the two drawn cards
        for i, card_path_or_surface in enumerate(drawn_cards):
            if isinstance(card_path_or_surface, pygame.Surface):
                card_image = card_path_or_surface
            else:
                card_image = pygame.image.load(card_path_or_surface)
            card_rect = card_image.get_rect(center=(WIDTH // 2 + (i - 0.5) * 150, HEIGHT // 2 + 50))
            screen.blit(card_image, card_rect.topleft)
        pygame.display.flip()
        # Wait for player input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 2 or event.button == 3):
                x, y = event.pos
                for i, card_rect in enumerate([card_rect for i in range(2)]):
                    card_rect.topleft = (WIDTH // 2 + (i - 0.5) * 150, HEIGHT // 2 + 50)
                    if card_rect.collidepoint(x, y):
                        selected_card_index = i
    # Get the file path for the selected card
    selected_card_path = drawn_cards[selected_card_index]
 
    player_rack_images.append(selected_card_path)
 
    # Remove the selected card from the pool
    pool_images.remove(selected_card_path)
    # Draw the player's rack with the new card
    selected_image = pygame.image.load(selected_card_path)
    player_images.append(selected_image)
 
 
def select_valid_group_or_run(image_paths, num_tiles):
    while True:
        selected_tiles = random.sample(image_paths, num_tiles)
        tile_numbers = [int(tile.split('_')[1]) for tile in selected_tiles]
        if is_valid_group_or_run(tile_numbers):
            return selected_tiles
 
def get_current_player_rack_images():
    return player_rack_images.copy()
   
def get_player_rack_images():
    return player_rack_images
 
# Variables for player and computer scores
player_score = 0
computer_score = 0

# Create Rect object for the combined score box
combined_score_box_rect = pygame.Rect(WIDTH - 150, 10, 120, 80)
computer_score_box_rect = pygame.Rect(WIDTH - 160, 10, 120, 80)
 
def is_valid_group_or_run_fin(tile_paths):
    # Exclude lists of just one length
    if len(tile_paths) <= 2:
        return "Invalid"
    # Extract tile numbers and colors
    tile_info = [(int(tile.split('_')[1]), tile.split('_')[2]) for tile in tile_paths]
    # Check if it's a run
    if all(num % 2 == tile_info[0][0] % 2 and color == tile_info[0][1] for num, color in tile_info):
        return "Run"
    # Check if it's a group
    if all(num == tile_info[0][0] for num, color in tile_info) and len(set(color for num, color in tile_info)) == len(tile_info):
        return "Group"
 
    # Check for invalid case with length 3
    if len(tile_paths) >= 3 and (any(tile_info.count(tile) > 1 for tile in tile_info) or len(set(tile_info)) < len(tile_info)):
        return "Invalid"
 
    return "Invalid"
 
 
score_list = []
 
scored_minilists = set()
 
def calculate_score(minilists):
    total_score = 0
    scored_minilists.clear()
    score_list.clear()
 
    for minilist in minilists:
        # Convert the minilist to a tuple to make it hashable and check if it's scored before
        minilist_tuple = tuple(minilist)
        if minilist_tuple not in scored_minilists:
            result = is_valid_group_or_run_fin(minilist)
            if result == "Group" or result == "Run":
                tile_numbers = [int(tile.split('_')[1]) for tile in minilist]
                total_score += sum(tile_numbers)
           
            # Mark the minilist as scored
            scored_minilists.add(minilist_tuple)
 
    score_list.append(total_score)
 
    return sum(score_list)
 
 
def remove_card_from_grid(game_board_grid, selected_card_path):
    filename = os.path.basename(selected_card_path)
    desired_part = filename.split('.')[0]
 
    # Remove from game_board_tiles
    for index, tile_info in enumerate(game_board_tiles):
        if desired_part in tile_info['selected image path']:
            print(tile_info['selected image path'])
            del game_board_tiles[index]
 
    for row in game_board_grid:
        for cell in row:
            if cell['image_path'] is not None and desired_part in cell['image_path']:
                cell['image_path'] = None
               
def perform_ct_button_click():
    global combination_found, computer_rack_images, pool_images, game_board_tiles, computer_images
 
    # Check if it's the computer's turn
    if not dragging and not game_board_dragging:
        combination_found = False
 
        # Check for a sequence of the same number with different colors in the computer's rack
        for number in range(1, 16):  # Check for numbers 1 to 13
            same_number_images = [image for image in computer_rack_images if int(image.split('_')[1]) == number]
 
            if len(same_number_images) >= 3:
                # Sort images by color to form a sequence
                same_number_images.sort(key=lambda x: x.split('_')[2])
 
                # Choose a random subset of the sequence (minimum 3, maximum 5 cards)
                subset_size = random.randint(3, min(len(same_number_images), 5))
                selected_images = random.sample(same_number_images, subset_size)
 
                # Simulate placing the selected cards on the game board
                col = random.randint(0, num_columns - subset_size)
                row = random.randint(0, num_rows - 1)
 
                if is_valid_group_or_run_fin(same_number_images) == "Invalid":
                    combination_found = False
                    break
 
                # Check if the selected cells on the game board are empty
                if all(game_board_grid[row][col + i]['image_path'] is None for i in range(subset_size)):
                    for i, image_path in enumerate(selected_images):
                        game_board_grid[row][col + i]['image_path'] = image_path
                        game_board_tiles.append({
                            'image': pygame.image.load(os.path.join("C:\\path_to_images", image_path)),
                            'rect': pygame.Rect(game_board_grid[row][col + i]['cell_rect']),
                            'selected image path': image_path
                        })
 
                        # Remove the selected card from the computer's rack
                        computer_rack_images.remove(image_path)
 
                    if is_valid_group_or_run_fin(same_number_images) in ("Run", "Group"):
                        combination_found = True
 
                    break
 
        # If no sequence is found, draw a card from the pool
        if not combination_found:
            if len(pool_images) > 0:
                drawn_card = random.choice(pool_images)
                computer_rack_images.append(drawn_card)
 
                # Remove the drawn card from the pool
                pool_images.remove(drawn_card)
 
        # Update computer_images after the move
        computer_images = [pygame.image.load(os.path.join("C:\\path_to_images", path)) for path in computer_rack_images] 
 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        if event.type == timer_event:
            if not play_button_clicked:
                current_time -= 1
                if current_time <= 0:
                    print(f"{current_player}'s turn is over!")
                    current_time = total_time
                    if current_player == "Player":
                        current_player = "Computer"
                        freeze_panel()
                    else:
                        current_player = "Player"
                        unfreeze_panel()
 
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
 
                # Check if the mouse click is on a player's image
                for i, image in enumerate(player_images):
                    rect = image.get_rect(topleft=(player_rack_rect.left + scroll_offset_player + i * (image.get_width() + spacing),
                                                   player_rack_rect.centery - image.get_height() // 2))
                    if rect.collidepoint(x, y):
                        dragging = True
                        selected_image = image
                        selected_index = i
                        original_position = rect.topleft
 
                # Check if the mouse click is on an image on the game board
                for i, tile in enumerate(game_board_tiles):
                    if tile['rect'].collidepoint(x, y):
                        game_board_dragging = True
                        game_board_selected_index = i
                        selected_image = tile['image']
                        original_position = tile['rect'].topleft
 
                if play_button_rect.collidepoint(x, y):
                    #print(f'Game Board Tiles : {game_board_tiles}')
                    groups_and_runs_main_list.clear()
                    for row in game_board_grid:
                         for cell in row:
                             image_path = cell['image_path']
                             groups_and_runs_main_list.append(image_path)
 
                    for item in groups_and_runs_main_list:
                        if item is not None:
                            current_mini_list.append(item)
                        elif current_mini_list:
                            mini_lists.append(current_mini_list)
                            current_mini_list = []
 
                    if current_mini_list:
                        mini_lists.append(current_mini_list)
 
                    current_mini_list.clear()
 
                    filtered_fin_list = [mini_list for mini_list in mini_lists if mini_list != [None]]
 
                    removal_lists_set = {tuple(inner_list) for inner_list in filtered_fin_list}
 
                    distinct_lists = [list(inner_tuple) for inner_tuple in removal_lists_set]
 
                    final_removal_distinct_list = [i for i in distinct_lists if len(i) in range(1,3)]
 
                    for image_paths_list in final_removal_distinct_list:
                        for selected_image_removal in image_paths_list:
                            if selected_image_removal not in player_rack_images:
                                player_rack_images.append(selected_image_removal)
                                selected_image_rem = pygame.image.load(selected_image_removal)
                                player_images.append(selected_image_rem)
                                filename = os.path.basename(selected_image_removal)
                                desired_part = filename.split('.')[0]
                                print(f'Selected Image Path for Removal : {desired_part}')
                                remove_card_from_grid(game_board_grid,desired_part)      
 
                    groups_and_runs_main_list.clear()
 
                    result_list = [
                        [os.path.splitext(os.path.basename(path))[0] for path in card_list]
                        for card_list in filtered_fin_list
                    ]
 
                    filtered_fin_list.clear()
                   
                    player_score = calculate_score(result_list)
                    result_list.clear()
 
                    print("Play Button Clicked!")
                    perform_ct_button_click()
                    current_time = total_time
                    current_player = "Computer"
                    play_button_clicked = True
                    freeze_panel()

                elif play_for_me_button_rect.collidepoint(x, y):
 
                    # Check if it's the player's turn
                    if not dragging and not game_board_dragging:
                        combination_found = False
 
                        # Iterate through each number to find a combination
                        for number in range(1, 16):  # Check for numbers 1 to 13
                            same_number_images = [image for image in player_rack_images if int(image.split('_')[1]) == number]
 
                            if len(same_number_images) >= 3:
                                # Sort images by color to form a sequence
                                same_number_images.sort(key=lambda x: x.split('_')[2])
 
                                # Choose a random subset of the sequence (minimum 3, maximum 5 cards)
                                subset_size = random.randint(3, min(len(same_number_images), 5))
                                selected_images = random.sample(same_number_images, subset_size)
 
                                # Simulate placing the selected cards on the game board
                                col = random.randint(0, num_columns - subset_size)
                                row = random.randint(0, num_rows - 1)
 
                                if is_valid_group_or_run_fin(same_number_images) == "Invalid":
                                    combination_found = False
                                    break
 
                                # Check if the selected cells on the game board are empty
                                if all(game_board_grid[row][col + i]['image_path'] is None for i in range(subset_size)):
                                    for i, image_path in enumerate(selected_images):
                                        game_board_grid[row][col + i]['image_path'] = image_path
                                        game_board_tiles.append({
                                            'image': pygame.image.load(os.path.join("C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project\\images\\", image_path)),
                                            'rect': pygame.Rect(game_board_grid[row][col + i]['cell_rect']),
                                            'selected image path': image_path
                                        })
 
                                        # Remove the selected card from the player's rack
                                        player_rack_images.remove(image_path)
 
                                    if is_valid_group_or_run_fin(same_number_images) in ("Run","Group"):
                                        combination_found = True
                                    break
 
                        # If no combination is found, draw a card from the pool
                        if not combination_found and len(pool_images) > 0:
                            drawn_card = random.choice(pool_images)
                            player_rack_images.append(drawn_card)
 
                            # Remove the drawn card from the pool
                            pool_images.remove(drawn_card)
 
                        # Update player_hand_images after the move
                        player_images = [pygame.image.load(os.path.join("C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project\\images\\", path)) for path in player_rack_images]
                        perform_ct_button_click()
 
                elif group_button_rect.collidepoint(x, y):
 
                    def sort_images_by_group(image_paths):
                        # Extract numbers from image paths
                        numbers = [int(image.split('_')[1]) for image in image_paths]
                        # Create a dictionary to store images based on numbers
                        images_by_number = {}
                        for number, path in zip(numbers, image_paths):
                            if number not in images_by_number:
                                images_by_number[number] = []
                            images_by_number[number].append(path)
                        # Sort the images based on numbers
                        sorted_images = []
                        for number in sorted(images_by_number.keys()):
                            sorted_images.extend(images_by_number[number])
                        return sorted_images
                   
                    # Sort player_rack_images
                    player_rack_images = sort_images_by_group(get_player_rack_images())
                    player_images = [pygame.image.load(os.path.join(base_path_1, path)) for path in player_rack_images]
 
                elif run_button_rect.collidepoint(x, y):
                    # Handle run button click
                    def sort_images_by_run(image_paths):
                        # Extract colors and numbers from image paths
                        color_number_pairs = [(image.split('_')[2], int(image.split('_')[1])) for image in image_paths]
                       
                        # Sort images based on colors and numbers
                        sorted_images = sorted(color_number_pairs, key=lambda x: (x[0], x[1]))
                       
                        # Convert back to image paths
                        sorted_image_paths = [f"tile_{num}_{color}" for color, num in sorted_images]
                        return sorted_image_paths
                   
                    player_rack_images = sort_images_by_run(player_rack_images)
                    # Load images
                    base_image_path = "C:\\Users\\sanyo\\Rummikub-Presentation\\Rummikub-Project"
                    player_images = [pygame.image.load(os.path.join(base_image_path, "images", path)) if "images" in path else pygame.image.load(os.path.join(base_image_path, "images-1", path)) for path in player_rack_images]
 
 
                elif pool_button_rect.collidepoint(x, y):
                    draw_cards_from_pool()
 
                elif show_all_tiles_rect.collidepoint(x, y):
                    show_computer_rack = not show_computer_rack
 
                elif group_button_rect.collidepoint(x, y):
                    if player_rack_images:
                        remaining_deck_images += player_rack_images
                    player_rack_images = []
                    current_state = get_current_player_rack_images()
                    print("Current player rack state:", current_state)
 
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                x, y = event.pos
                # Update the position of the selected image
                selected_image_rect = selected_image.get_rect(center=(x, y))
                dragged_image_rect = selected_image_rect  # Update the rect of the dragged image
                player_images[selected_index] = selected_image
 
            # If an image on the game board is being dragged, update its position
            if game_board_dragging:
                x, y = event.pos
 
                # Find the cell in the grid that the mouse is over
                col = max(0, min((x - game_board_rect.left) // cell_width, num_columns - 1))
                row = max(0, min((y - game_board_rect.top) // cell_height, num_rows - 1))
               
                # Update the position of the dragged image on the game board based on the grid
                game_board_tiles[game_board_selected_index]['rect'].topleft = game_board_grid[row][col]['cell_rect'].topleft
 
 
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                # Check if the mouse is released over the game board
                x, y = event.pos
                if game_board_rect.collidepoint(x, y):
 
                    # Find the cell in the grid that the mouse is over
                    col = max(0, min((x - game_board_rect.left) // cell_width, num_columns - 1))
                    row = max(0, min((y - game_board_rect.top) // cell_height, num_rows - 1))
                    # Place the image path on the game board grid
                    game_board_grid[row][col]['image_path'] = player_rack_images[selected_index]
 
                    # Place the image on the game board
                    game_board_tiles.append({
                        'image': selected_image,
                        'rect': selected_image_rect,
                        'selected image path': player_rack_images[selected_index]
                    })
 
                    del player_rack_images[selected_index]
                    del player_images[selected_index]
                else:
                    # Return the image to its original position
                    player_images[selected_index] = selected_image
                dragging = False
                selected_image = None
                selected_index = None
                original_position = None
                dragged_image_rect = None  # Reset the rect of the dragged image
 
            # If an image on the game board was being dragged, reset the dragging state
            if game_board_dragging:
                game_board_dragging = False
                game_board_selected_index = None
 
           
 
    # Draw background
    screen.blit(background_image, (0, 0))
 
    screen.blit(top_left_image, (10, 20))
 
    # Draw buttons
    pygame.draw.rect(screen, (0, 255, 0), play_button_rect)  # Green color for play button
    pygame.draw.rect(screen, (255, 0, 0), group_button_rect)  # Red color for Group button
    pygame.draw.rect(screen, (255, 0, 0), run_button_rect)  # Red color for Run button
    pygame.draw.rect(screen, (0, 0, 255), pool_button_rect)  # Blue color for pool button
    pygame.draw.rect(screen, (255, 165, 0), show_all_tiles_rect) # Orange color for pool button
    pygame.draw.rect(screen, (255, 165, 0), play_for_me_button_rect) # Orange color for pool button
 
    # Draw game board and racks
    pygame.draw.rect(screen, BROWN, game_board_rect)  # White color for the game board
    pygame.draw.rect(screen, WHITE, player_rack_rect)  # White color for player's rack
    pygame.draw.rect(screen, WHITE, computer_rack_rect)  # White color for computer's rack
 
    # Draw text boxes for Player and Computer labels
    player_label_rect = pygame.Rect(10, player_rack_rect.top, 80, player_rack_rect.height)
    computer_label_rect = pygame.Rect(10, computer_rack_rect.top, 80, computer_rack_rect.height)
 
    pygame.draw.rect(screen, (195, 120, 92), player_label_rect)  # White color for player label box
    pygame.draw.rect(screen, (195, 120, 92), computer_label_rect)  # White color for computer label box
 
    # Draw Player and Computer labels centered in the text boxes
    player_text = italic_font.render("Player", True, WHITE)  # White color for text
    player_text_rect = player_text.get_rect(center=player_label_rect.center)
    screen.blit(player_text, player_text_rect.topleft)
 
    computer_text = italic_font.render("Computer", True, WHITE)  # White color for text
    computer_text_rect = computer_text.get_rect(center=computer_label_rect.center)
    screen.blit(computer_text, computer_text_rect.topleft)
 
    # Draw Rummikub heading at the top of the player's rack
    rummikub_heading = custom_font.render("Rummikub", True, WHITE)
    rummikub_heading_rect = rummikub_heading.get_rect(center=(player_rack_rect.centerx, player_rack_rect.top - 50))
    screen.blit(rummikub_heading, rummikub_heading_rect.topleft)
 
    # Draw player rack images with scrolling
    for i, image in enumerate(player_images):
        x = player_rack_rect.left + scroll_offset_player + i * (image.get_width() + spacing)
        y = player_rack_rect.centery - image.get_height() // 2
        if player_rack_rect.left + scroll_offset_player + (i + 1) * (image.get_width() + spacing) < player_rack_rect.right:
            screen.blit(image, (x, y))
 
    # Draw computer rack images with scrolling if show_computer_rack is True
    if show_computer_rack:
        for i, image in enumerate(computer_images):
            x = computer_rack_rect.left + scroll_offset_computer + i * (image.get_width() + spacing)
            y = computer_rack_rect.centery - image.get_height() // 2
            if computer_rack_rect.left + scroll_offset_computer + (i + 1) * (image.get_width() + spacing) < computer_rack_rect.right:
                screen.blit(image, (x, y))

 
    play_for_me_button_font = pygame.font.Font(None, 28)
    text_play_for_me = play_for_me_button_font.render("Play For Me", True, (255, 255, 255))  # White color for text
    text_play_for_me_rect = text_play_for_me.get_rect(center=play_for_me_button_rect.center)
    screen.blit(text_play_for_me, text_play_for_me_rect.topleft)
 
    text_play = font.render("Play", True, (255, 255, 255))
    text_play_rect = text_play.get_rect(center=play_button_rect.center)
    screen.blit(text_play, text_play_rect.topleft)
 
    text_group = font.render("777", True, (255, 255, 255))
    text_group_rect = text_group.get_rect(center=group_button_rect.center)
    screen.blit(text_group, text_group_rect.topleft)
 
    text_run = font.render("246", True, (255, 255, 255))
    text_run_rect = text_run.get_rect(center=run_button_rect.center)
    screen.blit(text_run, text_run_rect.topleft)
 
    text_show_all_tiles = font.render("Show All Tiles", True, (255, 255, 255))
    text_show_all_tiles_rect = text_show_all_tiles.get_rect(center=show_all_tiles_rect.center)
    screen.blit(text_show_all_tiles, text_show_all_tiles_rect.topleft)
 
    text_pool = font.render(f'Pool : {len(pool_images)}', True, (255, 255, 255))
    text_pool_rect = text_pool.get_rect(center=pool_button_rect.center)
    screen.blit(text_pool, text_pool_rect.topleft)
 
    if dragging:
        x, y = pygame.mouse.get_pos()
        screen.blit(selected_image, (x - selected_image.get_width() // 2, y - selected_image.get_height() // 2))
 
    # Draw the images on the game board
    for tile in game_board_tiles:
        screen.blit(tile['image'], tile['rect'].topleft)
 
    # Draw the game board grid
    for row in game_board_grid:
        for cell in row:
            pygame.draw.rect(screen, grid_stroke_color, cell['stroke_rect'], 1)
 
   
    pygame.draw.rect(screen, WHITE, combined_score_box_rect)
 
    text_player_score = font.render(f"Player: {player_score}", True, (0, 0, 0))
    text_computer_score = font.render(f"Computer: {computer_score}", True, (0, 0, 0))
   
    # Center the text within the box
    text_player_rect = text_player_score.get_rect(center=(combined_score_box_rect.centerx, combined_score_box_rect.centery - 15))
    text_computer_rect = text_computer_score.get_rect(center=(combined_score_box_rect.centerx, combined_score_box_rect.centery + 15))
 
    screen.blit(text_player_score, text_player_rect.topleft)
    screen.blit(text_computer_score, text_computer_rect.topleft)

    # Render the timer text
    timer_text = font.render(f"Timer : {current_time} seconds", True, WHITE)
    screen.blit(timer_text, (20, 640))
 
    # Render the timer and current player text
    timer_text = font.render(f"Time: {current_time} seconds", True, WHITE)
    player_text = font.render(f"Current Player: {current_player}", True, WHITE)
    screen.blit(player_text, (20, 670))
 
    # Reset the flag after handling the click event
    play_button_clicked = False
   
    pygame.display.flip()
    clock.tick(FPS)
 
pygame.quit()
