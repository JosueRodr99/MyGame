import pygame
import math
import random
from settings import *
try:
    from maze_designer import create_custom_level
except ImportError:
    create_custom_level = None
    
try:
    from sprite_loader import sprite_loader
except ImportError:
    sprite_loader = None

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usar sprite personalizado si está disponible
        if sprite_loader:
            self.image = sprite_loader.get_player_sprite()
        else:
            self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        
    def update(self, keys, walls):
        """Update player position based on input and collision with walls"""
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            
        # Move and check collisions
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx
            
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= dy
            
        # Keep player on screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        self.speed = ENEMY_SPEED
        self.hunt_mode_speed = ENEMY_SPEED * HUNT_MODE_ENEMY_SPEED_MULTIPLIER
        self.is_boss = False
        
        # Usar sprite personalizado si está disponible
        if sprite_loader:
            self.image = sprite_loader.get_enemy_sprite(enemy_type, False)
        else:
            if enemy_type == "circle":
                self.image = pygame.Surface((ENEMY_CIRCLE_SIZE, ENEMY_CIRCLE_SIZE))
                self.image.fill(ENEMY_CIRCLE_COLOR)
            elif enemy_type == "square":
                self.image = pygame.Surface((ENEMY_SQUARE_SIZE, ENEMY_SQUARE_SIZE))
                self.image.fill(ENEMY_SQUARE_COLOR)
            elif enemy_type == "triangle":
                self.image = pygame.Surface((ENEMY_TRIANGLE_SIZE, ENEMY_TRIANGLE_SIZE))
                self.image.fill(ENEMY_TRIANGLE_COLOR)
        if enemy_type == "circle":
            self.color = ENEMY_CIRCLE_COLOR
        elif enemy_type == "square":
            self.color = ENEMY_SQUARE_COLOR
        elif enemy_type == "triangle":
            self.color = ENEMY_TRIANGLE_COLOR
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # AI behavior
        self.direction = random.uniform(0, 2 * math.pi)
        self.change_direction_timer = 0
        self.change_direction_interval = random.randint(60, 180)  # frames
        
        # Hunt mode behavior
        self.is_in_hunt_mode = False
        self.gathering_timer = 0
        self.gathering_duration = 30  # frames
        
    def make_boss(self):
        """Convert this enemy to a boss"""
        self.is_boss = True
        self.speed = BOSS_SPEED
        self.hunt_mode_speed = BOSS_SPEED * HUNT_MODE_ENEMY_SPEED_MULTIPLIER
        
        # Increase size and use boss sprite
        old_center = self.rect.center
        if sprite_loader:
            self.image = sprite_loader.get_enemy_sprite(self.enemy_type, True)
        else:
            self.image = pygame.Surface((BOSS_SIZE, BOSS_SIZE))
            if self.enemy_type == "circle":
                self.image.fill(BOSS_CIRCLE_COLOR)
            elif self.enemy_type == "square":
                self.image.fill(BOSS_SQUARE_COLOR)
            elif self.enemy_type == "triangle":
                self.image.fill(BOSS_TRIANGLE_COLOR)
        if self.enemy_type == "circle":
            self.color = BOSS_CIRCLE_COLOR
        elif self.enemy_type == "square":
            self.color = BOSS_SQUARE_COLOR
        elif self.enemy_type == "triangle":
            self.color = BOSS_TRIANGLE_COLOR
            
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
    def update(self, player, walls, hunt_mode, gather_point=None):
        """Update enemy position and behavior"""
        current_speed = self.hunt_mode_speed if hunt_mode else self.speed
        
        if hunt_mode:
            self.is_in_hunt_mode = True
            if gather_point:
                # Move towards gather point
                dx = gather_point[0] - self.rect.centerx
                dy = gather_point[1] - self.rect.centery
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    dx = (dx / distance) * current_speed
                    dy = (dy / distance) * current_speed
                    
                    self.rect.x += dx
                    self.rect.y += dy
                    
                    # Check wall collisions
                    if pygame.sprite.spritecollide(self, walls, False):
                        self.rect.x -= dx
                        self.rect.y -= dy
        else:
            self.is_in_hunt_mode = False
            # Normal AI behavior
            self.change_direction_timer += 1
            
            if self.change_direction_timer >= self.change_direction_interval:
                self.direction = random.uniform(0, 2 * math.pi)
                self.change_direction_timer = 0
                self.change_direction_interval = random.randint(60, 180)
            
            # Move in current direction
            dx = math.cos(self.direction) * current_speed
            dy = math.sin(self.direction) * current_speed
            
            self.rect.x += dx
            self.rect.y += dy
            
            # Check wall collisions and bounce
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x -= dx
                self.rect.y -= dy
                self.direction = random.uniform(0, 2 * math.pi)
            
            # Keep enemy on screen
            self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Usar sprite personalizado si está disponible
        if sprite_loader:
            self.image = sprite_loader.get_wall_sprite()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = None
        self.is_boss_level = level_num in [3, 6, 9]
        
        # Create level layout
        self.create_level_layout()
        
    def create_level_layout(self):
        """Create the maze layout for this level"""
        # Use the new custom level designer if available
        if create_custom_level:
            self.walls, self.enemies, self.player = create_custom_level(self.level_num)
        else:
            # Fallback to original method
            if self.level_num == 1:
                self.create_level_1()
            elif self.level_num == 2:
                self.create_level_2()
            elif self.level_num == 3:
                self.create_boss_level("circle")
            else:
                self.create_level_1()  # Default
            
    def create_level_1(self):
        """Create level 1 layout"""
        # Simple maze with basic enemies
        # Outer walls
        self.walls.add(Wall(0, 0, SCREEN_WIDTH, WALL_THICKNESS))
        self.walls.add(Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))
        self.walls.add(Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT))
        self.walls.add(Wall(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS))
        
        # Inner walls
        self.walls.add(Wall(200, 200, WALL_THICKNESS, 200))
        self.walls.add(Wall(400, 300, 200, WALL_THICKNESS))
        self.walls.add(Wall(600, 200, WALL_THICKNESS, 200))
        
        # Create enemies
        self.enemies.add(Enemy(100, 100, "circle"))
        self.enemies.add(Enemy(300, 400, "square"))
        self.enemies.add(Enemy(500, 100, "triangle"))
        
        # Create player
        self.player = Player(50, 50)
        
    def create_boss_level(self, boss_type):
        """Create a boss level"""
        # Outer walls
        self.walls.add(Wall(0, 0, SCREEN_WIDTH, WALL_THICKNESS))
        self.walls.add(Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))
        self.walls.add(Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT))
        self.walls.add(Wall(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS))
        
        # Create boss enemy
        boss = Enemy(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, boss_type)
        boss.make_boss()
        self.enemies.add(boss)
        
        # Add some regular enemies
        for i in range(3):
            enemy = Enemy(random.randint(100, SCREEN_WIDTH - 100), 
                         random.randint(100, SCREEN_HEIGHT - 100), 
                         random.choice(["circle", "square", "triangle"]))
            self.enemies.add(enemy)
        
        # Create player
        self.player = Player(50, 50)
        
    def create_level_2(self):
        """Create level 2 layout"""
        # Similar to level 1 but with more complexity
        self.create_level_1()  # Base layout
        # Add more walls and enemies
        self.walls.add(Wall(300, 100, WALL_THICKNESS, 100))
        self.walls.add(Wall(500, 400, 100, WALL_THICKNESS))
        self.enemies.add(Enemy(700, 300, "circle"))
        self.enemies.add(Enemy(150, 500, "square"))
        
    def create_level_4(self):
        """Create level 4 layout"""
        self.create_level_1()  # Base layout
        # Add more complexity
        self.walls.add(Wall(100, 300, 200, WALL_THICKNESS))
        self.walls.add(Wall(600, 100, WALL_THICKNESS, 300))
        self.enemies.add(Enemy(400, 500, "triangle"))
        self.enemies.add(Enemy(800, 200, "circle"))
        self.enemies.add(Enemy(200, 600, "square"))
        
    def create_level_5(self):
        """Create level 5 layout"""
        self.create_level_4()  # Base layout
        # Add even more complexity
        self.walls.add(Wall(400, 200, WALL_THICKNESS, 200))
        self.walls.add(Wall(200, 400, 300, WALL_THICKNESS))
        self.enemies.add(Enemy(600, 600, "triangle"))
        self.enemies.add(Enemy(100, 200, "circle"))
        
    def create_level_7(self):
        """Create level 7 layout"""
        self.create_level_5()  # Base layout
        # Add more walls and enemies
        self.walls.add(Wall(500, 500, 200, WALL_THICKNESS))
        self.walls.add(Wall(300, 600, WALL_THICKNESS, 100))
        self.enemies.add(Enemy(700, 500, "square"))
        self.enemies.add(Enemy(150, 300, "triangle"))
        
    def create_level_8(self):
        """Create level 8 layout"""
        self.create_level_7()  # Base layout
        # Final regular level before final boss
        self.walls.add(Wall(600, 300, WALL_THICKNESS, 200))
        self.walls.add(Wall(100, 500, 400, WALL_THICKNESS))
        self.enemies.add(Enemy(800, 400, "circle"))
        self.enemies.add(Enemy(300, 700, "square"))
        self.enemies.add(Enemy(500, 100, "triangle"))
