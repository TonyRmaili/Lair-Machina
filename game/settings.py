import pygame_menu


def custom_theme(theme_name: str = 'THEME_DARK'):
    # Dynamically retrieve the theme using getattr
    theme = getattr(pygame_menu.themes, theme_name).copy()  # Get the theme by name and copy it
    
    theme.title_font_color = (255, 215, 0)  # Set title color to gold
    theme.widget_font_color = (0, 255, 0)  # Set button text color to green
    theme.background_color = (50, 50, 50)  # Set the background to a dark grey
    theme.widget_font = pygame_menu.font.FONT_FRANCHISE  # Custom font (optional)

    return theme