import pygame
from sprites import Wall, Enemy, Player
from settings import *
import random

class MazeDesigner:
    """
    Herramienta para diseñar laberintos personalizados
    """
    
    @staticmethod
    def create_maze_from_pattern(level_num, pattern=None):
        """
        Crea un laberinto basado en un patrón de texto
        
        Patrón:
        '#' = Pared
        '.' = Espacio libre
        'P' = Posición del jugador
        'E' = Enemigo
        'B' = Jefe
        """
        
        walls = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = None
        
        # Patrones predefinidos para cada nivel
        patterns = {
            1: [
                "###################",
                "#P........#......#",
                "#.#######.#.####.#",
                "#.#.....#.#.#..#.#",
                "#.#.###.#.#.#.##.#",
                "#.#.#...#.#.#..#.#",
                "#.#.#.###.#.####.#",
                "#.#.#.....#....#.#",
                "#.#.#########.##.#",
                "#.#...........#.#",
                "#.#############.#",
                "#...............#",
                "###################"
            ],
            2: [
                "###################",
                "#P....#...#......#",
                "#.###.#.#.#.####.#",
                "#...#.#.#.#.#..#.#",
                "###.#.#.#.#.#.##.#",
                "#...#.#...#.#..#.#",
                "#.###.#####.####.#",
                "#....#.....#....#.",
                "####.#.###.#.###.#",
                "#....#.#...#.#...#",
                "#.######.#.###.###",
                "#........#.....#E#",
                "###################"
            ],
            3: [
                "###################",
                "#P...............#",
                "#.###############.#",
                "#.#...........#.#.#",
                "#.#.#########.#.#.#",
                "#.#.#.......#.#.#.#",
                "#.#.#.#####.#.#.#.#",
                "#.#.#.#...#.#.#.#.#",
                "#.#.#.#.#.#.#.#.#.#",
                "#.#.#.#...#.#.#.#.#",
                "#.#.#.#####.#.#.#.#",
                "#.#.#.......#.#.#.#",
                "#.#.#########.#.#.#",
                "#.#...........#.#.#",
                "#.###############.#",
                "#...............B#",
                "###################"
            ]
        }
        
        if pattern is None:
            pattern = patterns.get(level_num, patterns[1])
        
        # Dimensiones del patrón
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        
        # Calcular tamaño de cada celda
        cell_width = SCREEN_WIDTH // pattern_width
        cell_height = SCREEN_HEIGHT // pattern_height
        
        # Crear laberinto basado en el patrón
        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                cell_x = x * cell_width
                cell_y = y * cell_height
                
                if cell == '#':  # Pared
                    walls.add(Wall(cell_x, cell_y, cell_width, cell_height))
                elif cell == 'P':  # Jugador
                    player = Player(cell_x + cell_width//2, cell_y + cell_height//2)
                elif cell == 'E':  # Enemigo
                    enemy_type = random.choice(["circle", "square", "triangle"])
                    enemies.add(Enemy(cell_x + cell_width//2, cell_y + cell_height//2, enemy_type))
                elif cell == 'B':  # Jefe
                    boss_type = "circle" if level_num == 3 else "square" if level_num == 6 else "triangle"
                    boss = Enemy(cell_x + cell_width//2, cell_y + cell_height//2, boss_type)
                    boss.make_boss()
                    enemies.add(boss)
        
        return walls, enemies, player
    
    @staticmethod
    def create_custom_maze(level_num):
        """
        Crea un laberinto personalizado usando coordenadas específicas
        """
        walls = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        
        # Laberintos personalizados para cada nivel
        if level_num == 1:
            # Laberinto simple tipo "maze"
            walls.add(Wall(0, 0, SCREEN_WIDTH, WALL_THICKNESS))  # Top
            walls.add(Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))  # Left
            walls.add(Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT))  # Right
            walls.add(Wall(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS))  # Bottom
            
            # Paredes internas
            walls.add(Wall(200, 200, WALL_THICKNESS, 200))
            walls.add(Wall(400, 300, 200, WALL_THICKNESS))
            walls.add(Wall(600, 200, WALL_THICKNESS, 200))
            walls.add(Wall(300, 500, 300, WALL_THICKNESS))
            walls.add(Wall(700, 100, WALL_THICKNESS, 300))
            
            # Enemigos
            enemies.add(Enemy(100, 100, "circle"))
            enemies.add(Enemy(500, 400, "square"))
            enemies.add(Enemy(800, 200, "triangle"))
            
            player = Player(50, 50)
            
        elif level_num == 2:
            # Laberinto más complejo
            walls.add(Wall(0, 0, SCREEN_WIDTH, WALL_THICKNESS))
            walls.add(Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))
            walls.add(Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT))
            walls.add(Wall(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS))
            
            # Paredes internas más complejas
            walls.add(Wall(150, 150, WALL_THICKNESS, 200))
            walls.add(Wall(300, 200, 200, WALL_THICKNESS))
            walls.add(Wall(500, 150, WALL_THICKNESS, 250))
            walls.add(Wall(200, 400, 400, WALL_THICKNESS))
            walls.add(Wall(600, 300, WALL_THICKNESS, 200))
            walls.add(Wall(750, 150, WALL_THICKNESS, 300))
            walls.add(Wall(150, 600, 600, WALL_THICKNESS))
            
            # Enemigos
            enemies.add(Enemy(100, 100, "circle"))
            enemies.add(Enemy(350, 250, "square"))
            enemies.add(Enemy(650, 350, "triangle"))
            enemies.add(Enemy(400, 500, "circle"))
            enemies.add(Enemy(800, 200, "square"))
            
            player = Player(50, 50)
            
        elif level_num == 3:  # Boss level
            # Laberinto para jefe
            walls.add(Wall(0, 0, SCREEN_WIDTH, WALL_THICKNESS))
            walls.add(Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))
            walls.add(Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT))
            walls.add(Wall(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS))
            
            # Arena central para el jefe
            walls.add(Wall(300, 200, WALL_THICKNESS, 200))
            walls.add(Wall(500, 200, WALL_THICKNESS, 200))
            walls.add(Wall(300, 200, 200, WALL_THICKNESS))
            walls.add(Wall(300, 400, 200, WALL_THICKNESS))
            
            # Jefe
            boss = Enemy(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "circle")
            boss.make_boss()
            enemies.add(boss)
            
            # Enemigos adicionales
            enemies.add(Enemy(150, 150, "square"))
            enemies.add(Enemy(800, 600, "triangle"))
            
            player = Player(50, 50)
            
        else:
            # Niveles adicionales
            walls, enemies, player = MazeDesigner.create_maze_from_pattern(level_num)
        
        return walls, enemies, player
    
    @staticmethod
    def create_spiral_maze(level_num):
        """
        Crea un laberinto en espiral
        """
        walls = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        
        # Paredes exteriores
        walls.add(Wall(0, 0, SCREEN_WIDTH, WALL_THICKNESS))
        walls.add(Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))
        walls.add(Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT))
        walls.add(Wall(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS))
        
        # Espiral
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        for i in range(5):
            radius = 100 + i * 80
            # Paredes en espiral
            walls.add(Wall(center_x - radius, center_y - radius, radius * 2, WALL_THICKNESS))
            walls.add(Wall(center_x - radius, center_y + radius - WALL_THICKNESS, radius * 2, WALL_THICKNESS))
            walls.add(Wall(center_x - radius, center_y - radius, WALL_THICKNESS, radius * 2))
            walls.add(Wall(center_x + radius - WALL_THICKNESS, center_y - radius, WALL_THICKNESS, radius * 2))
        
        # Enemigos en posiciones estratégicas
        enemies.add(Enemy(center_x - 200, center_y - 200, "circle"))
        enemies.add(Enemy(center_x + 200, center_y - 200, "square"))
        enemies.add(Enemy(center_x - 200, center_y + 200, "triangle"))
        enemies.add(Enemy(center_x + 200, center_y + 200, "circle"))
        
        player = Player(50, 50)
        
        return walls, enemies, player

# Función para usar en sprites.py
def create_custom_level(level_num):
    """
    Función principal para crear niveles personalizados
    """
    if level_num <= 3:
        return MazeDesigner.create_custom_maze(level_num)
    elif level_num <= 6:
        return MazeDesigner.create_maze_from_pattern(level_num)
    else:
        return MazeDesigner.create_spiral_maze(level_num)
