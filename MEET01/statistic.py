class Statistic:
    # intro = False
    # game_active = True

    intro = True
    game_active = False
    play_again = True

    high_score = 0
    level = 1
    life = 3
    score = 0

    @staticmethod
    def reset_game():
        Statistic.score = 0
        Statistic.level = 1
        Statistic.life = 3
    
