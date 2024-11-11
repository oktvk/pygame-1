import pygame
import os  # Add this import statement
from conf import Conf

class Life(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets/life.png"))  # Load life image
        self.image = pygame.transform.scale(self.image, (30, 30))  # Scale the image if needed
        self.rect = self.image.get_rect()

    def show(self):
        # This method is called to draw the life icon on the screen
        for i in range(Statistic.life):
            # Position the life icons
            self.game.screen.blit(self.image, (10 + i * 35, 10))  # Adjust position as needed