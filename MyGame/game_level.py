import pygame
import sys
import math
import random
from sprites import *
from settings import *
from audio import audio_manager

class GameLevel:
    def __init__(self, level_num):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"MAZE HUNT - Level {level_num}")
        self.clock = pygame.time.Clock()
        
        # Level data
        self.level_num = level_num
        self.level = Level(level_num)
        
        # Game state
        self.running = True
        self.game_time = 0  # Total game time in seconds
        self.hunt_mode_active = False
        self.hunt_mode_start_time = 0
        self.hunt_mode_duration = HUNT_MODE_DURATION
        self.hunt_mode_cooldown = HUNT_MODE_COOLDOWN
        self.last_hunt_mode_time = -HUNT_MODE_COOLDOWN  # Allow first hunt mode immediately
        
        # Game objects
        self.all_sprites = pygame.sprite.Group()
        self.walls = self.level.walls
        self.enemies = self.level.enemies
        self.player = self.level.player
        
        # Add to sprite groups
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemies)
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        
        # Gather point for hunt mode
        self.gather_point = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        
        # Game over state
        self.game_over = False
        self.victory = False
        
        # Play level music
        audio_manager.play_music('level_music', loops=-1)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "lobby"
                elif event.key == pygame.K_SPACE and not self.hunt_mode_active:
                    # Try to activate hunt mode
                    current_time = pygame.time.get_ticks() / 1000
                    if current_time - self.last_hunt_mode_time >= self.hunt_mode_cooldown:
                        self.activate_hunt_mode()
                        
        return True
        
    def activate_hunt_mode(self):
        """Activate hunt mode"""
        self.hunt_mode_active = True
        self.hunt_mode_start_time = pygame.time.get_ticks() / 1000
        self.last_hunt_mode_time = self.hunt_mode_start_time
        
        # Play hunt mode sound
        audio_manager.play_sound('hunt_mode_start')
        
        # Play hunt music
        audio_manager.play_music('hunt_music', loops=-1)
        
    def deactivate_hunt_mode(self):
        """Deactivate hunt mode"""
        self.hunt_mode_active = False
        
        # Play hunt mode end sound
        audio_manager.play_sound('hunt_mode_end')
        
        # Return to level music
        audio_manager.play_music('level_music', loops=-1)
        
    def update(self):
        """Update game logic"""
        if self.game_over:
            return
            
        current_time = pygame.time.get_ticks() / 1000
        
        # Update game time (only when not in hunt mode)
        if not self.hunt_mode_active:
            self.game_time = current_time
            
        # Check hunt mode duration
        if self.hunt_mode_active:
            hunt_elapsed = current_time - self.hunt_mode_start_time
            if hunt_elapsed >= self.hunt_mode_duration:
                self.deactivate_hunt_mode()
                
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.walls)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.walls, self.hunt_mode_active, self.gather_point)
            
        # Check collisions between player and enemies
        if self.hunt_mode_active:
            # Player can kill enemies in hunt mode
            enemies_hit = pygame.sprite.spritecollide(self.player, self.enemies, True)
            for enemy in enemies_hit:
                audio_manager.play_sound('enemy_death')
        else:
            # Player dies if touched by enemies
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                self.game_over = True
                audio_manager.play_sound('player_hit')
                
        # Check victory condition
        if len(self.enemies) == 0:
            self.victory = True
            self.game_over = True
            audio_manager.play_sound('level_complete')
            
        # Check time limit
        if self.game_time >= GAME_TIME_LIMIT:
            self.game_over = True
            
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw walls
        self.walls.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy_type = enemy.enemy_type
            if enemy.is_boss:
                size = BOSS_SIZE
            else:
                if enemy_type == "circle":
                    size = ENEMY_CIRCLE_SIZE
                elif enemy_type == "square":
                    size = ENEMY_SQUARE_SIZE
                elif enemy_type == "triangle":
                    size = ENEMY_TRIANGLE_SIZE
                    
            # Draw enemy shape
            if enemy_type == "circle":
                pygame.draw.circle(self.screen, enemy.color, enemy.rect.center, size // 2)
            elif enemy_type == "square":
                pygame.draw.rect(self.screen, enemy.color, enemy.rect)
            elif enemy_type == "triangle":
                # Draw triangle
                points = [
                    (enemy.rect.centerx, enemy.rect.top),
                    (enemy.rect.left, enemy.rect.bottom),
                    (enemy.rect.right, enemy.rect.bottom)
                ]
                pygame.draw.polygon(self.screen, enemy.color, points)
                
        # Draw player
        pygame.draw.rect(self.screen, PLAYER_COLOR, self.player.rect)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def draw_ui(self):
        """Draw user interface"""
        # Game time
        time_text = f"Time: {int(self.game_time)}/{GAME_TIME_LIMIT}s"
        time_surface = self.font.render(time_text, True, self.WHITE)
        self.screen.blit(time_surface, (10, 10))
        
        # Enemies remaining
        enemies_text = f"Enemies: {len(self.enemies)}"
        enemies_surface = self.font.render(enemies_text, True, self.WHITE)
        self.screen.blit(enemies_surface, (10, 50))
        
        # Level number
        level_text = f"Level: {self.level_num}"
        level_surface = self.font.render(level_text, True, self.WHITE)
        self.screen.blit(level_surface, (10, 90))
        
        # Hunt mode indicator
        if self.hunt_mode_active:
            hunt_time_left = self.hunt_mode_duration - (pygame.time.get_ticks() / 1000 - self.hunt_mode_start_time)
            hunt_text = f"HUNT MODE: {int(hunt_time_left)}s"
            hunt_surface = self.font.render(hunt_text, True, self.RED)
            self.screen.blit(hunt_surface, (SCREEN_WIDTH // 2 - 100, 10))
        else:
            # Show hunt mode cooldown
            cooldown_left = self.hunt_mode_cooldown - (pygame.time.get_ticks() / 1000 - self.last_hunt_mode_time)
            if cooldown_left > 0:
                cooldown_text = f"Hunt Mode: {int(cooldown_left)}s"
                cooldown_surface = self.small_font.render(cooldown_text, True, self.YELLOW)
                self.screen.blit(cooldown_surface, (SCREEN_WIDTH // 2 - 80, 10))
            else:
                space_text = "Press SPACE for Hunt Mode"
                space_surface = self.small_font.render(space_text, True, self.GREEN)
                self.screen.blit(space_surface, (SCREEN_WIDTH // 2 - 100, 10))
                
        # Instructions
        instructions = [
            "WASD/Arrows: Move",
            "SPACE: Hunt Mode",
            "ESC: Exit"
        ]
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, self.WHITE)
            self.screen.blit(inst_surface, (SCREEN_WIDTH - 150, 10 + i * 25))
            
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        if self.victory:
            text = "VICTORY!"
            color = self.GREEN
        else:
            text = "GAME OVER"
            color = self.RED
            
        game_over_surface = pygame.font.Font(None, 72).render(text, True, color)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)
        
        # Instructions
        if self.victory:
            inst_text = "All enemies defeated!"
        else:
            inst_text = "You were caught!"
            
        inst_surface = self.font.render(inst_text, True, self.WHITE)
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(inst_surface, inst_rect)
        
        # Continue instruction
        continue_text = "Press ESC to return to lobby"
        continue_surface = self.small_font.render(continue_text, True, self.WHITE)
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(continue_surface, continue_rect)
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            result = self.handle_events()
            
            if result == False:
                running = False
            elif result == "lobby":
                return "lobby"
                
            # Update game
            self.update()
            
            # Draw everything
            self.draw()
            
            # Limit FPS
            self.clock.tick(FPS)
            
        return False

if __name__ == "__main__":
    # Test with level 1
    game = GameLevel(1)
    result = game.run()
    if result:
        print(f"Returning to: {result}")
    pygame.quit()
    sys.exit()
