import pygame
import os

from conf import Conf

class Bird():

    def __init__(self, Game):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect
        
        image_path = os.path.join(Conf.BASE_DIR, "assets", "bird.png")
        self.image = pygame.image.load(image_path)
        self.original_image = self.image  # this
        self.rect = self.image.get_rect()
        self.fly = False
        self.pass_pipe = False

        self.rect.center = self.screen_rect.center
        
        # angle awal
        self.angle = 0  

    def move(self):
        # untuk mengupdate angle burung
        if self.fly:
            self.angle += 5  # naik
        else:
            self.angle -= 5  # tutun

        # limit angle
        self.angle = max(-30, min(30, self.angle))

        # mengatur gerak burung
        if self.fly:
            self.rect.y -= Conf.BIRD_FLY_SPEED
        else:
            self.rect.y += Conf.GRAVITY

        # memutar burung
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # update rect agar update ke centre
        self.rect = self.image.get_rect(center=self.rect.center)

    def show(self):
        self.screen.blit(self.image, self.rect)