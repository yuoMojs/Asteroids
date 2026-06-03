import random
import pygame
from constants import *
from circleshape import CircleShape
from logger import log_event  # Import log_event for analytics tracking

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap()

    def split(self) -> None:
        # Always remove the current asteroid from play immediately
        self.kill()

        # If it's a small asteroid, we are done splitting
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Log the split event
        log_event("asteroid_split")

        # Determine a random angle of separation
        random_angle = random.uniform(20, 50)

        # Create two new distinct directional vectors
        vector1 = self.velocity.rotate(random_angle)
        vector2 = self.velocity.rotate(-random_angle)

        # Calculate the smaller size of the child fragments
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Instantiate two child fragments at the current impact position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Assign the new velocities and scale their speed up by 1.2x
        asteroid1.velocity = vector1 * 1.2
        asteroid2.velocity = vector2 * 1.2
