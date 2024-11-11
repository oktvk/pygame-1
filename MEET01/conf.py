import os

class Conf():

    BASE_DIR = os.path.dirname(__file__)
    FPS = 25
    SCREEN_SIZE = (500, 500) 
    SCREEN_BG_COLOR = (107, 52, 235)
    PLATFORM_SPEED = 5
    BIRD_FLY_SPEED = 3
    GRAVITY = 2

    PIPE_COLOR = (0, 200, 0)
    PIPE_SPEED = 5

    FONT_FAMILY = "CollegeGames.ttf"
    FONT_SIZE = 80
    FONT_COLOR = (242, 255, 0)

    BUTTON_FONT_SIZE = int(0.5*FONT_SIZE)
    BUTTON_WIDTH = 90
    BUTTON_HEIGHT = 50

    ENTRY_HEIGHT = 50
    ENTRY_COLOR_ACTIVE = (255, 0, 0)
    ENTRY_COLOR_INACTIVE = (122, 255, 200)
    ENTRY_FONT = "CollegeGames.ttf"
    ENTRY_FONT_SIZE = 30
    ENTRY_FONT_COLOR = (255, 255, 255)  