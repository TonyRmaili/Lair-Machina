import pygame
import pygame_menu
import sys
from debug import debug


class Game:
    def __init__(self):
        # setup
        self.FPS = 30
        self.WIDTH = 800
        self.HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Lair Machina")

        self.menu = pygame_menu.Menu('Welcome Adventurer', 400,300,
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Name :', default='John Doe')
        # self.menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        
        self.game_active = False


    def set_difficulty(self):
        pass

    def start_the_game(self):
        
        self.game_active = True
        

    def run(self):
        while True:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    
            if self.game_active:
                self.screen.fill('white')
                # You can add more game logic here
            else:
                # Show the menu if the game hasn't started yet
                self.menu.mainloop(self.screen)
            
                          
            pygame.display.flip()           
            self.clock.tick(self.FPS)

            debug(f'Game State: {self.game_active}',(10,10))
   
if __name__ == '__main__':
    game = Game()
    game.run()

    