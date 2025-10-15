import pygame
import sys
from settings import *
from audio import audio_manager

class Options:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MAZE HUNT - Options")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.LIGHT_GRAY = (192, 192, 192)
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER = (150, 150, 150)
        self.SLIDER_COLOR = (200, 200, 200)
        self.SLIDER_ACTIVE = (100, 150, 255)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Volume settings
        self.master_volume = audio_manager.master_volume
        self.music_volume = audio_manager.music_volume
        self.sfx_volume = audio_manager.sfx_volume
        self.brightness = 1.0
        
        # Slider settings
        self.slider_width = 200
        self.slider_height = 20
        self.slider_x = SCREEN_WIDTH // 2 - self.slider_width // 2
        
        # Slider rectangles
        self.master_slider = pygame.Rect(self.slider_x, 200, self.slider_width, self.slider_height)
        self.music_slider = pygame.Rect(self.slider_x, 280, self.slider_width, self.slider_height)
        self.sfx_slider = pygame.Rect(self.slider_x, 360, self.slider_width, self.slider_height)
        self.brightness_slider = pygame.Rect(self.slider_x, 440, self.slider_width, self.slider_height)
        
        # Slider handles
        self.master_handle = pygame.Rect(self.slider_x + int(self.master_volume * self.slider_width) - 10, 195, 20, 30)
        self.music_handle = pygame.Rect(self.slider_x + int(self.music_volume * self.slider_width) - 10, 275, 20, 30)
        self.sfx_handle = pygame.Rect(self.slider_x + int(self.sfx_volume * self.slider_width) - 10, 355, 20, 30)
        self.brightness_handle = pygame.Rect(self.slider_x + int(self.brightness * self.slider_width) - 10, 435, 20, 30)
        
        # Buttons
        self.back_button = pygame.Rect(50, 50, 100, 40)
        self.reset_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 550, 200, 50)
        
        # Button states
        self.back_hover = False
        self.reset_hover = False
        
        # Dragging states
        self.dragging_master = False
        self.dragging_music = False
        self.dragging_sfx = False
        self.dragging_brightness = False
        
    def draw_slider(self, rect, handle_rect, value, label):
        """Draw a volume slider"""
        # Draw slider background
        pygame.draw.rect(self.screen, self.SLIDER_COLOR, rect)
        pygame.draw.rect(self.screen, self.DARK_GRAY, rect, 2)
        
        # Draw slider handle
        pygame.draw.rect(self.screen, self.SLIDER_ACTIVE, handle_rect)
        pygame.draw.rect(self.screen, self.WHITE, handle_rect, 2)
        
        # Draw label
        label_surface = self.label_font.render(label, True, self.WHITE)
        self.screen.blit(label_surface, (rect.x - 150, rect.y - 5))
        
        # Draw value
        value_text = f"{int(value * 100)}%"
        value_surface = self.small_font.render(value_text, True, self.WHITE)
        self.screen.blit(value_surface, (rect.x + rect.width + 10, rect.y - 5))
        
    def draw_button(self, rect, text, hover, font):
        """Draw a button with hover effect"""
        color = self.BUTTON_HOVER if hover else self.BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.WHITE, rect, 2)
        
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def update_slider_value(self, slider_rect, mouse_x):
        """Update slider value based on mouse position"""
        relative_x = mouse_x - slider_rect.x
        value = max(0.0, min(1.0, relative_x / slider_rect.width))
        return value
        
    def update_handle_position(self, handle_rect, slider_rect, value):
        """Update slider handle position based on value"""
        handle_rect.x = slider_rect.x + int(value * slider_rect.width) - 10
        handle_rect.x = max(slider_rect.x - 10, min(handle_rect.x, slider_rect.x + slider_rect.width - 10))
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEMOTION:
                # Check button hover states
                self.back_hover = self.back_button.collidepoint(event.pos)
                self.reset_hover = self.reset_button.collidepoint(event.pos)
                
                # Handle slider dragging
                if self.dragging_master:
                    self.master_volume = self.update_slider_value(self.master_slider, event.pos[0])
                    self.update_handle_position(self.master_handle, self.master_slider, self.master_volume)
                    audio_manager.set_master_volume(self.master_volume)
                    
                elif self.dragging_music:
                    self.music_volume = self.update_slider_value(self.music_slider, event.pos[0])
                    self.update_handle_position(self.music_handle, self.music_slider, self.music_volume)
                    audio_manager.set_music_volume(self.music_volume)
                    
                elif self.dragging_sfx:
                    self.sfx_volume = self.update_slider_value(self.sfx_slider, event.pos[0])
                    self.update_handle_position(self.sfx_handle, self.sfx_slider, self.sfx_volume)
                    audio_manager.set_sfx_volume(self.sfx_volume)
                    
                elif self.dragging_brightness:
                    self.brightness = self.update_slider_value(self.brightness_slider, event.pos[0])
                    self.update_handle_position(self.brightness_handle, self.brightness_slider, self.brightness)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check slider handles
                    if self.master_handle.collidepoint(event.pos):
                        self.dragging_master = True
                    elif self.music_handle.collidepoint(event.pos):
                        self.dragging_music = True
                    elif self.sfx_handle.collidepoint(event.pos):
                        self.dragging_sfx = True
                    elif self.brightness_handle.collidepoint(event.pos):
                        self.dragging_brightness = True
                        
                    # Check buttons
                    elif self.back_button.collidepoint(event.pos):
                        return "lobby"
                    elif self.reset_button.collidepoint(event.pos):
                        self.reset_to_defaults()
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    self.dragging_master = False
                    self.dragging_music = False
                    self.dragging_sfx = False
                    self.dragging_brightness = False
                    
        return True
        
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.master_volume = MASTER_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        self.brightness = 1.0
        
        # Update audio manager
        audio_manager.set_master_volume(self.master_volume)
        audio_manager.set_music_volume(self.music_volume)
        audio_manager.set_sfx_volume(self.sfx_volume)
        
        # Update handle positions
        self.update_handle_position(self.master_handle, self.master_slider, self.master_volume)
        self.update_handle_position(self.music_handle, self.music_slider, self.music_volume)
        self.update_handle_position(self.sfx_handle, self.sfx_slider, self.sfx_volume)
        self.update_handle_position(self.brightness_handle, self.brightness_slider, self.brightness)
        
    def run(self):
        """Main options loop"""
        running = True
        
        while running:
            # Handle events
            result = self.handle_events()
            
            if result == False:
                running = False
            elif result == "lobby":
                return "lobby"
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw title
            title_text = "OPTIONS"
            title_surface = self.title_font.render(title_text, True, self.WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title_surface, title_rect)
            
            # Draw sliders
            self.draw_slider(self.master_slider, self.master_handle, self.master_volume, "Master Volume")
            self.draw_slider(self.music_slider, self.music_handle, self.music_volume, "Music Volume")
            self.draw_slider(self.sfx_slider, self.sfx_handle, self.sfx_volume, "SFX Volume")
            self.draw_slider(self.brightness_slider, self.brightness_handle, self.brightness, "Brightness")
            
            # Draw buttons
            self.draw_button(self.back_button, "BACK", self.back_hover, self.label_font)
            self.draw_button(self.reset_button, "RESET TO DEFAULTS", self.reset_hover, self.label_font)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
            
        return False

if __name__ == "__main__":
    options = Options()
    result = options.run()
    if result:
        print(f"Returning to: {result}")
    pygame.quit()
    sys.exit()
