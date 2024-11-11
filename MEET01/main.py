import pygame
import sys
import os
from random import choice

from conf import Conf
from statistic import Statistic
from sprites.platform import Platform
from sprites.bird import Bird
from sprites.pipe import Pipe
from sprites.life import Life  # Add this line


from sprites.basics.label import Label
from sprites.basics.button import PlayButton, Button , MuteButton
from sprites.basics.entry import Entry

class Game:

    pygame.init()
    screen = pygame.display.set_mode(Conf.SCREEN_SIZE)
    screen_rect = screen.get_rect()
    

    def __init__(self):
        self.mute_button = MuteButton(self, "MUTE")
        self.is_muted = False  # Track the mute state
        self.life_image = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets/life.png")) #
        self.life_image = pygame.transform.scale(self.life_image, (30, 30)) #
        self.game_title_label = Label(self, "Flappy Bird")
        # self.player_entry = Entry(self, "player")
        self.login_button = Button(self, "LOGIN")
        # self.play_button = PlayButton(self)
        self.play_button = Button(self, "PLAY NOW")

        self.play_again_button = Button(self, "PLAY AGAIN")
        self.exit_button = Button(self, "EXIT")
        self.reposition_play_again_and_exit_button()

        self.platform = Platform(self)
        self.bird = Bird(self)
        self.pipes = [ Pipe(self, position) for position in ["top", "bottom"] ]
        self.life = Life(self)

        self.play_backsound("wandering.wav")

    def play_backsound(self, song):
        pygame.mixer.music.load(os.path.join(Conf.BASE_DIR, "assets/sound", song))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play(loops=-1)

    def draw_lives(self):
        for i in range(Statistic.life):
            self.screen.blit(self.life_image, (10 + i * 35, 10))  #

    def draw_score(self):
        font = pygame.font.Font(None, 36)  # 
        score_surface = font.render(f"Score: {Statistic.score}", True, (255, 255, 255))  # warna
        self.screen.blit(score_surface, (10, 90))  # 

    def reposition_play_again_and_exit_button(self):
        self.play_again_button.rect.y -= 70
        self.play_again_button.text_image_rect.centery= self.play_again_button.rect.centery + 10

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.set_volume(0)  # Mute

        else:
            pygame.mixer.music.set_volume(1)  # 


    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.fly = True

            elif event.type == pygame.KEYUP:    
                if event.key == pygame.K_SPACE:
                    self.bird.fly = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if Statistic.intro:
                    self.check_onclick_login_button(mouse_pos)
                elif Statistic.play_again:
                    self.check_onclick_exit_button(mouse_pos)
                    self.check_onclick_play_again_button(mouse_pos)
                elif not Statistic.game_active:
                    self.check_onclick_play_button(mouse_pos)
                # Check for mute button click
                if self.mute_button.check_click(mouse_pos):
                    self.toggle_mute()
                

    def check_onclick_login_button(self, mouse_pos):
        if self.login_button.rect.collidepoint(mouse_pos):
            Statistic.intro = False

    def check_onclick_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            Statistic.game_active = True
    
    def check_onclick_exit_button(self, mouse_pos):
        print(mouse_pos)
        if self.exit_button.rect.collidepoint(mouse_pos):
            sys.exit()

    def check_onclick_play_again_button(self, mouse_pos):
        if self.play_again_button.rect.collidepoint(mouse_pos):
            if Statistic.life > 0:  # 
                print("play again")
                self.reset_pipes()
                self.bird.rect.center = self.screen_rect.center
                Statistic.play_again = False
                Statistic.game_active = True
            else:
                print("No lives left. Game Over.")

    def check_bird_get_point(self):
        for pipe in self.pipes:
            if (pipe.rect.centerx <= self.bird.rect.centerx) and not self.bird.pass_pipe:
                self.bird.pass_pipe = True
                Statistic.score += 10
                if Statistic.high_score < Statistic.score:
                    Statistic.high_score = Statistic.score
                print(Statistic.score)

    def check_bird_hit_pipe_or_platform(self):
        collision_pipes = pygame.sprite.spritecollideany(self.bird, self.pipes)
        collision_platform = pygame.Rect.colliderect(self.bird.rect, self.platform.rect)

        if collision_pipes or collision_platform:
            Statistic.life -= 1  # 
            if Statistic.life <= 0:
                Statistic.game_active = False
                Statistic.play_again = False  # Kalo hati sudah hilang, tidak bisa di minkan lagi
                print("Game Over! No lives left.")
            else:
                Statistic.play_again = True  #  Kalo masih ada hati, bisa di minkan lagi
                print(f"Lives left: {Statistic.life}")

    def set_fps(self):
        pygame.time.Clock().tick(Conf.FPS)
        pygame.display.flip()

    def reset_pipes(self):
        self.pipes[0].rect.topleft = self.screen_rect.topright
        self.pipes[1].rect.bottomleft = self.screen_rect.bottomright

        random_height = choice([25, 50, 75, 100, 125, 150])
        minimum_height = self.platform.rect.height + (0.1*self.screen_rect.height)
        new_height_bottom = minimum_height + random_height
        new_height_top = self.screen_rect.height - new_height_bottom - self.screen_rect.height//5

        self.pipes[1].rect = pygame.Rect(0, 0, 0.15*self.screen_rect.width, new_height_bottom)
        self.pipes[0].rect = pygame.Rect(0, 0, 0.15*self.screen_rect.width, new_height_top)

        self.pipes[1].rect.bottomleft = self.screen_rect.bottomright
        self.pipes[0].rect.topleft = self.screen_rect.topright

    def game_intro(self):
        self.game_title_label.show()
        # self.player_entry.show()
        self.login_button.show()

    def game_play(self):      
        self.bird.show()
        for pipe in self.pipes:              
            pipe.show()
        self.platform.show()
        
        self.draw_lives()  # 
        self.mute_button.show()  # 
        self.draw_score()  # /////

        if not Statistic.game_active and not Statistic.play_again:
            self.game_title_label.show()
            self.play_button.show()
        elif Statistic.play_again:
            self.play_again_button.show()
            self.exit_button.show()
        elif Statistic.game_active:    
            self.update_bird_activity()
            self.update_pipes_activity()
            self.update_platform_activity()
        elif Statistic.life <= 0:  # kons
            self.game_title_label.show()
            print("Game Over! You have no lives left.")


    def update_bird_activity(self):
        self.bird.move()
        self.check_bird_get_point()
        self.check_bird_hit_pipe_or_platform()

    def update_pipes_activity(self):
        for pipe in self.pipes:
            if pipe.rect.right <= 0:
                self.reset_pipes()
                self.bird.pass_pipe = False               
            pipe.move()

    def update_platform_activity(self):
        self.platform.move()
        


    def loop(self):
        while True:
            self.screen.fill(Conf.SCREEN_BG_COLOR)  

            if Statistic.intro:
                self.game_intro()
            else:
                self.game_play()
            
            self.set_fps()
            self.check_event()

if __name__ == "__main__":
    game = Game()
    game.loop() 