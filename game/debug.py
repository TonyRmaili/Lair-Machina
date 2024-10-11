import pygame
pygame.init()

font= pygame.font.Font(None,20)

def debug(info,pos):
    """
    can be inserted in the main loop to display debug info - will get output on the screen - a text window that console logs the info 
    """
    display_surface= pygame.display.get_surface()
    debug_surf= font.render(str(info),True,'white')
    debug_rect= debug_surf.get_rect(topleft=(pos))
    pygame.draw.rect(display_surface,'black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)
