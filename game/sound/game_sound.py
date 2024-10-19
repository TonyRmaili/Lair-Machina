import pygame
import sys
import os
# from text_handler import TextHandler
# from tts import TTSGame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from widgets.button import Button

class GameSound:
    def __init__(self):
        self.FPS = 60
        self.WIDTH = 945
        self.HEIGHT = 650
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.play_sound = Button(pos=(300,400),text_input='Play Sound',
                            base_color="black", hovering_color="Green") 
        
        pygame.display.set_caption("Sound Machina")

    
    def run(self):
        while True:  
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.play_sound.changeColor(position=mouse_pos)

            for event in events:
                # handles quits 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_sound.checkForInput(position=mouse_pos):
                        print('playing sound')

            self.screen.fill('white')  
            self.play_sound.draw(screen=self.screen)
            pygame.display.flip()           
            self.clock.tick(self.FPS)

   
if __name__ == '__main__':
    game = GameSound()
    game.run()