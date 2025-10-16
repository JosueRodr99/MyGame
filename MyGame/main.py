import pygame
import sys
import os
from lobby import Lobby
from levels import LevelSelection
from options import Options
from game_level import GameLevel
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MAZE HUNT")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game states
        self.current_state = "lobby"
        self.lobby = Lobby()
        self.level_selection = LevelSelection()
        self.options = Options()
        
        # Game settings
        self.brightness = 1.0
        self.master_volume = MASTER_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        
    def run(self):
        """Main game loop"""
        while self.running:
            if self.current_state == "lobby":
                result = self.lobby.run()
                if result == "levels":
                    self.current_state = "levels"
                elif result == "options":
                    self.current_state = "options"
                elif result == False:
                    self.running = False
                    
            elif self.current_state == "levels":
                result = self.level_selection.run()
                if result == "lobby":
                    self.current_state = "lobby"
                elif result and isinstance(result, str) and result.startswith("level_"):
                    # Start the actual game level
                    level_num = int(result.split("_")[1])
                    self.start_level(level_num)
                elif result == False:
                    self.running = False
                    
            elif self.current_state == "options":
                result = self.options.run()
                if result == "lobby":
                    self.current_state = "lobby"
                elif result == False:
                    self.running = False
                
            elif self.current_state.startswith("game_level_"):
                level_num = int(self.current_state.split("_")[2])
                game_level = GameLevel(level_num)
                result = game_level.run()
                if result == "lobby":
                    self.current_state = "lobby"
                elif result == False:
                    self.running = False
                
            # Limit FPS
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def start_level(self, level_num):
        """Start a specific game level"""
        print(f"Starting level {level_num}")
        # TODO: Implement actual game level logic
        self.current_state = f"game_level_{level_num}"

if __name__ == "__main__":
    game = Game()
    game.run()
