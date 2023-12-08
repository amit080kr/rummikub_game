# Rummikub_Project_Group 9

Welcome to the Rummikub project! This project is a Python implementation of the Rummikub game using the Pygame library. Dive into the world of Rummikub and enjoy the game right on your computer!

## Set up 
1. **Use git clone to load the Repository locally:**
   - git clone <repo_url>
   - After cloning it locally the Repository will be created in local directory.

2. **Folder Structure:**
   The extracted folder structure should look like this:
   Pygame
└── Rummikub-Project
    ├── images
    ├── images-1
    ├── AbrilFatface-Regular.ttf
    ├── wood.png
    ├── README.md
    ├── Game_screenshot_Group_9.png
    ├── Final_pygame.py
    ├── .DS_Store
    └── logo.png

    
3. **Assets Placement:**
- **Background Image:** Place the `wood.png` file in the `Rummikub-Project` folder.
- **Font File:** The font file `AbrilFatface-Regular.ttf` should be in the root of the `Rummikub-Project` folder.

## Usage/Examples

Now that you have set up the project, you can use the provided code snippet to load the background image, fonts, and other assets in your Python script.

```python
import pygame

# Set the dimensions of the window
WIDTH = 800
HEIGHT = 600

# Initialize Pygame
pygame.init()

# Load background image
background_image = pygame.image.load("Pygame/Rummikub-Project/wood.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Adding and Loading the Images
base_path_1 = "Pygame/Rummikub-Project/images/"
base_path_2 = "Pygame/Rummikub-Project/images-1/"
colors = ["blue", "yellow", "red", "orange", "green"]

# Load a custom font file
custom_font = pygame.font.Font("Pygame/Rummikub-Project/AbrilFatface-Regular.ttf", 36)

## Features

- **Interactive Gameplay:** Experience the thrill of Rummikub with a user-friendly interface and interactive gameplay.
- **Beautiful Graphics:** Enjoy visually appealing graphics, including a dynamic background and vibrant tile designs.
- **Font Customization:** Stand out with a unique visual style using the included custom font.
- **Diverse Images:** Explore the game's visual richness with a variety of images from the respective folders.

## Repository

Explore the code and stay updated on our [GitHub Repository](https://gitlab.com/rummikub-game-project/Rummikub-Project.git).

##  Visuals

![Screenshot](https://gitlab.com/rummikub-game-project/Rummikub-Project/-/raw/main/Game_screenshot_Group_9.png?ref_type=heads)

## Authors

- Sanyog Chavhan (psxsc24)
- Rohan Sood (psxrs14)
- Girija Dahibhate(psxgd2)
- Ayush Ranjan (psxar8)
- Amit Kumar (psxak21)

