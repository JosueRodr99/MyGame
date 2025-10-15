import pygame
import sys
import os
from settings import *

class Lobby:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MAZE HUNT")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.LIGHT_GRAY = (192, 192, 192)
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER = (150, 150, 150)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        
        # Button rectangles
        self.play_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
        self.options_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50)
        
        # Button states
        self.play_hover = False
        self.options_hover = False
        
    def draw_pixelated_text(self, text, font, color, x, y):
        """Draw text with a pixelated effect"""
        # Create the main text
        text_surface = font.render(text, True, color)
        
        # Create a shadow effect for pixelated look
        shadow_surface = font.render(text, True, self.DARK_GRAY)
        
        # Draw shadow offset
        self.screen.blit(shadow_surface, (x + 2, y + 2))
        
        # Draw main text
        self.screen.blit(text_surface, (x, y))
        
        # Add some pixelated highlights
        highlight_surface = font.render(text, True, self.LIGHT_GRAY)
        self.screen.blit(highlight_surface, (x - 1, y - 1))
        
    def draw_button(self, rect, text, hover, font):
        """Draw a button with hover effect"""
        color = self.BUTTON_HOVER if hover else self.BUTTON_COLOR
        
        # Draw button background
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.WHITE, rect, 2)
        
        # Draw button text
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEMOTION:
                # Check button hover states
                self.play_hover = self.play_button.collidepoint(event.pos)
                self.options_hover = self.options_button.collidepoint(event.pos)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.play_button.collidepoint(event.pos):
                        return "levels"
                    elif self.options_button.collidepoint(event.pos):
                        return "options"
        
        return True
        
    def run(self):
        """Main lobby loop"""
        running = True
        
        while running:
            # Handle events
            result = self.handle_events()
            
            if result == False:
                running = False
            elif result == "levels":
                return "levels"
            elif result == "options":
                return "options"
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw title
            title_text = "MAZE HUNT"
            title_surface = self.title_font.render(title_text, True, self.GRAY)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
            self.draw_pixelated_text(title_text, self.title_font, self.GRAY, title_rect.x, title_rect.y)
            
            # Draw buttons
            self.draw_button(self.play_button, "PLAY", self.play_hover, self.button_font)
            self.draw_button(self.options_button, "OPTIONS", self.options_hover, self.button_font)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
            
        return False

if __name__ == "__main__":
    lobby = Lobby()
    result = lobby.run()
    if result:
        print(f"Transitioning to: {result}")
    pygame.quit()
    sys.exit()
