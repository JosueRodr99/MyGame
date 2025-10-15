import pygame
import sys
from settings import *

class LevelSelection:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MAZE HUNT - Select Level")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.LIGHT_GRAY = (192, 192, 192)
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER = (150, 150, 150)
        self.BOSS_COLOR = (255, 100, 100)
        self.BOSS_HOVER = (255, 150, 150)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.level_font = pygame.font.Font(None, 24)
        self.back_font = pygame.font.Font(None, 36)
        
        # Level buttons (3x3 grid)
        self.level_buttons = []
        self.level_hovers = [False] * 9
        
        # Calculate positions for 3x3 grid
        start_x = SCREEN_WIDTH // 2 - (3 * LEVEL_BUTTON_SIZE + 2 * LEVEL_BUTTON_MARGIN) // 2
        start_y = SCREEN_HEIGHT // 2 - (3 * LEVEL_BUTTON_SIZE + 2 * LEVEL_BUTTON_MARGIN) // 2
        
        for i in range(9):
            row = i // 3
            col = i % 3
            x = start_x + col * (LEVEL_BUTTON_SIZE + LEVEL_BUTTON_MARGIN)
            y = start_y + row * (LEVEL_BUTTON_SIZE + LEVEL_BUTTON_MARGIN)
            self.level_buttons.append(pygame.Rect(x, y, LEVEL_BUTTON_SIZE, LEVEL_BUTTON_SIZE))
        
        # Back button
        self.back_button = pygame.Rect(50, 50, 100, 40)
        self.back_hover = False
        
        # Boss levels (3, 6, 9)
        self.boss_levels = [2, 5, 8]  # 0-indexed
        
    def is_boss_level(self, level_index):
        """Check if a level is a boss level"""
        return level_index in self.boss_levels
        
    def draw_level_button(self, rect, level_num, hover, is_boss):
        """Draw a level button with appropriate styling"""
        if is_boss:
            color = self.BOSS_HOVER if hover else self.BOSS_COLOR
        else:
            color = self.BUTTON_HOVER if hover else self.BUTTON_COLOR
            
        # Draw button background
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw border
        border_color = self.WHITE if not is_boss else (255, 200, 200)
        pygame.draw.rect(self.screen, border_color, rect, 3)
        
        # Draw level number
        text_surface = self.level_font.render(str(level_num), True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Draw boss indicator
        if is_boss:
            boss_text = self.level_font.render("BOSS", True, self.WHITE)
            boss_rect = boss_text.get_rect(center=(rect.centerx, rect.centery + 15))
            self.screen.blit(boss_text, boss_rect)
            
    def draw_back_button(self, rect, hover):
        """Draw the back button"""
        color = self.BUTTON_HOVER if hover else self.BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.WHITE, rect, 2)
        
        text_surface = self.back_font.render("BACK", True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEMOTION:
                # Check level button hover states
                for i, button in enumerate(self.level_buttons):
                    self.level_hovers[i] = button.collidepoint(event.pos)
                    
                # Check back button hover
                self.back_hover = self.back_button.collidepoint(event.pos)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check level buttons
                    for i, button in enumerate(self.level_buttons):
                        if button.collidepoint(event.pos):
                            return f"level_{i + 1}"
                    
                    # Check back button
                    if self.back_button.collidepoint(event.pos):
                        return "lobby"
        
        return True
        
    def run(self):
        """Main level selection loop"""
        running = True
        
        while running:
            # Handle events
            result = self.handle_events()
            
            if result == False:
                running = False
            elif result == "lobby":
                return "lobby"
            elif result and isinstance(result, str) and result.startswith("level_"):
                return result
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw title
            title_text = "SELECT LEVEL"
            title_surface = self.title_font.render(title_text, True, self.WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title_surface, title_rect)
            
            # Draw level buttons
            for i, button in enumerate(self.level_buttons):
                level_num = i + 1
                is_boss = self.is_boss_level(i)
                self.draw_level_button(button, level_num, self.level_hovers[i], is_boss)
            
            # Draw back button
            self.draw_back_button(self.back_button, self.back_hover)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
            
        return False

if __name__ == "__main__":
    level_selection = LevelSelection()
    result = level_selection.run()
    if result:
        print(f"Selected: {result}")
    pygame.quit()
    sys.exit()
