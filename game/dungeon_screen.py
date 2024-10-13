import pygame
import sys
from image import Image
from textarea import TextArea
from input_text import InputText
from button import Button
import ollama

large_text = '''
**The Ancient Era (Before the Common Era 1000 - 500)**

1. **The Elyrian Empire's Ascendancy**: A vast, magically governed empire rose to power, its dominion stretching across Eridoria. The Elyrians mastered elemental magic, using it to maintain control and prosperity.

2. **The Valtorian Federation's Formation**: As the Elyrian Empire expanded, a loose alliance of city-states known as the Valtorians emerged in response. They emphasized democracy and technological innovation over magical prowess.

**The Era of Expansion (Before the Common Era 500 - 100)**

1. **The Great Conjunction**: A rare celestial event where the planets aligned, granting immense magical power to those who harnessed it. This led to an era of great discovery and advancement in magic and technology, as empires sought to capitalize on this newfound energy.

2. **The Elyrian-Valtorian War**: A protracted conflict that ravaged the land, pitting the magical prowess of the Elyrians against the technological might of the Valtorians. The war ended with a fragile peace treaty, but it marked the beginning of the decline of both empires.

**The Era of Ascendancy (Before the Common Era 100 - 500)**

1. **The Rise of the Kyrean Kingdom**: Through strategic alliances and innovations in technology, the Kyreans expanded their empire, absorbing smaller states and rival city-states.

2. **The Discovery of Aerthys**: A continent hidden beyond Eridoria's known lands was discovered by the Kyreans, leading to a surge in trade, knowledge, and cultural exchange.

**The Era of Decline (Common Era 500 - 1000)**

1. **The Great Devastation**: A cataclysmic event caused by an unstable artifact from the Elyrian Empire. This disaster led to widespread destruction, altering global climates, geography, and ecosystems.

2. **The Schism of the Gods**: As a response to the devastation, the pantheons of gods began to fracture, with some deities advocating for intervention in mortal affairs while others advocated for withdrawal.

**The Era of Renaissance (Common Era 1000 - 1500)**

1. **The Revival of Learning**: A period of intellectual and artistic flowering, as scholars rediscovered ancient knowledge and civilizations rose anew from the ashes of the Great Devastation.

2. **The Reunification Wars**: As old rivalries resurfaced, empires clashed in a series of wars that reshaped the world order, with some kingdoms rising to new heights while others fell into decline.

**Pivotal Moments**

1. **The Discovery of the Celestial Tome**: An ancient text containing powerful magic and knowledge from the dawn of time. Its discovery has led to numerous quests for its translation and mastery.

2. **The Awakening of the Ancient Ones**: Legends speak of ancient beings who slumbered beneath the earth, waiting for their chance to reclaim their places in the world. Their awakening is said to bring either salvation or catastrophe.

**Cosmic Forces**

1. **The Balance of Elements**: The universe operates under a delicate balance between elements (earth, air, fire, water). Imbalances can cause global calamities or grant immense power to those who master them.

2. **The Dance of the Stars**: Eridoria's celestial movements influence global events. Rare alignments have brought prosperity while others foretold disaster.

**Key Civilizations**

1. **The Elyrian Empire**: Though fallen, their legacy in magic lives on, with remnants seeking to reclaim their former glory.

2. **The Kyrean Kingdom**: The technological might of the Kyreans has become a hallmark of power and innovation.

3. **The Valtorian Federation**: Despite internal strife, they remain a potent force for democracy and unity.

4. **The Wysteria Confederation**: A recent rising power that champions magic as the solution to Eridoria's problems.

**Ancient Prophecies**

1. **The Great Unification**: An ancient prophecy foretells of a world unified under one rule, with peace and prosperity for all. However, its interpretation is open to debate.

2. **The Last Age**: A prophecy speaks of the coming age where civilization will collapse under the weight of greed, power struggles, and environmental degradation.

This complex history sets the stage for ongoing conflicts, alliances, and quests in Eridoria. Ancient prophecies, magical discoveries, and technological advancements have shaped the world into its current state, setting the stage for further transformation.

'''

class DungeonSceen:
    """
    needs to be updated to merge with the game_map.py
    """
    def __init__(self,game,w,h):
        self.game = game
        path = './pics/'
        self.bg = Image(image=path+'floor.jpg',pos=(250,0),scale=(w-250,h-250))
        namepath = self.game.char.name
        path = './pics/'+ namepath + '/'
        # THIS NEEDS TO HAVE errorhandling/async - if the img or folder is not created yet
        self.character_image = Image(image=path+'ComfyUI_00019_.png',pos=(w-250,h-250),scale=(250,250))

        self.prompt_box = InputText(x=0,y=h-250,width=w-250,height=h-250,title='prompt box',bg_color=(69, 69, 69), text_color=(255, 255, 255))
        self.response_box = TextArea(text=large_text,WIDTH=250,HEIGHT=h-300,x=0,y=0,text_color=(255, 255, 255),bg_color=(69, 69, 69),title='response box',title_color='black')

        self.prompt_button = Button(pos=(w-325,h-275),text_input='Submit',image=None,base_color="black", hovering_color="Green",font=pygame.font.Font(None, 36))
        

    def ask_ollama(self,prompt):
        resp = ollama.generate(
            model='llama3.1',
            prompt=prompt
        )

        return resp['response']

    def handle_event(self,events):
        mouse_pos = pygame.mouse.get_pos()
        self.prompt_button.changeColor(position=mouse_pos)
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_q:
                    self.game.game_mode = 'menu'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.prompt_button.checkForInput(mouse_pos):
                    prompt =self.prompt_box.send_text()
                    # self.ask_ollama(prompt=prompt)
                    self.response_box.new_text(text=prompt)

            self.response_box.event_handler(event=event)

    def run(self,screen,events):
        self.handle_event(events=events)
        
        self.bg.update(screen=screen)

        self.character_image.update(screen=screen)
        self.prompt_box.draw(screen=screen,events=events)
        self.response_box.display(screen=screen)
        self.prompt_button.update(screen=screen)

        

       
        
        



