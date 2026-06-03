import sys
import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    score = 0
    lives = 3
    player = None
    game_state = "menu"

    def start_game():
        nonlocal player, score, lives, game_state
        # Wipe any sprites left over from a previous round before respawning
        for group in (updatable, drawable, asteroids, shots):
            group.empty()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()
        score = 0
        lives = 3
        game_state = "playing"

    def draw_centered(text, fnt, y, color="white"):
        surf = fnt.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH / 2, y)))

    # Game Loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if game_state in ("menu", "game_over"):
                    start_game()

        screen.fill("black")

        if game_state == "playing":
            # Update states
            updatable.update(dt)

            # Collision detection
            for asteroid in asteroids:
                if asteroid.collides_with(player) and player.invincible <= 0:
                    log_event("player_hit")
                    lives -= 1
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.velocity = pygame.Vector2(0, 0)
                    player.invincible = 3.0
                    if lives <= 0:
                        log_event("game_over")
                        game_state = "game_over"

                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        shot.kill()
                        score += int(asteroid.radius)
                        asteroid.split()

            # Render graphics
            for obj in drawable:
                obj.draw(screen)

            score_surf = font.render(f"Score: {score}", True, "white")
            screen.blit(score_surf, (10, 10))
            lives_surf = font.render(f"Lives: {lives}", True, "white")
            screen.blit(lives_surf, (10, 46))

        elif game_state == "menu":
            draw_centered("ASTEROIDS", big_font, SCREEN_HEIGHT / 2 - 40)
            draw_centered("Press ENTER to start", font, SCREEN_HEIGHT / 2 + 30)

        elif game_state == "game_over":
            # Keep the final frame of the field behind the overlay text
            for obj in drawable:
                obj.draw(screen)
            draw_centered("GAME OVER", big_font, SCREEN_HEIGHT / 2 - 40, "red")
            draw_centered(f"Final Score: {score}", font, SCREEN_HEIGHT / 2 + 20)
            draw_centered("Press ENTER to play again", font, SCREEN_HEIGHT / 2 + 60)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
