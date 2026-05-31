import pygame
from constants import *
from logger import log_state

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(
        f"Screen width: {SCREEN_WIDTH}\n"
        f"Screen height: {SCREEN_HEIGHT}"
    )
    
    # 1. Initialize pygame
    pygame.init()
    
    # 2. Set up the display window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 3. Game Loop
    while True:
        # Log the state at the start of the loop
        log_state()
        
        # Check for window close events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Fill the screen with black
        screen.fill("black")
        
        # Refresh the screen (always call this last in the loop)
        pygame.display.flip()

if __name__ == "__main__":
    main()
