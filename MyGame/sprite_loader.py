import pygame
import os
from settings import *

class SpriteLoader:
    """
    Sistema para cargar y manejar sprites personalizados
    """
    
    def __init__(self):
        self.sprites = {}
        self.images_path = "assets/Imagen"
        self.load_sprites()
    
    def load_sprites(self):
        """Carga todos los sprites desde la carpeta de imágenes"""
        # Crear directorio si no existe
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)
            print(f"Directorio {self.images_path} creado. Coloca tus sprites aquí.")
        
        # Cargar sprites específicos
        sprite_files = {
            'player': ['player.png', 'player.jpg', 'jugador.png'],
            'enemy_circle': ['enemy_circle.png', 'enemigo_circulo.png', 'circulo.png'],
            'enemy_square': ['enemy_square.png', 'enemigo_cuadrado.png', 'cuadrado.png'],
            'enemy_triangle': ['enemy_triangle.png', 'enemigo_triangulo.png', 'triangulo.png'],
            'boss_circle': ['boss_circle.png', 'jefe_circulo.png'],
            'boss_square': ['boss_square.png', 'jefe_cuadrado.png'],
            'boss_triangle': ['boss_triangle.png', 'jefe_triangulo.png'],
            'wall': ['wall.png', 'pared.png', 'muro.png'],
            'background': ['background.png', 'fondo.png']
        }
        
        for sprite_name, possible_files in sprite_files.items():
            sprite_loaded = False
            for filename in possible_files:
                filepath = os.path.join(self.images_path, filename)
                if os.path.exists(filepath):
                    try:
                        image = pygame.image.load(filepath)
                        # Redimensionar según el tipo de sprite
                        if 'player' in sprite_name:
                            image = pygame.transform.scale(image, (PLAYER_SIZE, PLAYER_SIZE))
                        elif 'enemy' in sprite_name or 'boss' in sprite_name:
                            if 'boss' in sprite_name:
                                image = pygame.transform.scale(image, (BOSS_SIZE, BOSS_SIZE))
                            else:
                                image = pygame.transform.scale(image, (ENEMY_CIRCLE_SIZE, ENEMY_CIRCLE_SIZE))
                        elif 'wall' in sprite_name:
                            image = pygame.transform.scale(image, (WALL_THICKNESS, WALL_THICKNESS))
                        
                        self.sprites[sprite_name] = image
                        sprite_loaded = True
                        print(f"Sprite cargado: {sprite_name} desde {filename}")
                        break
                    except pygame.error as e:
                        print(f"Error cargando {filename}: {e}")
            
            if not sprite_loaded:
                print(f"Sprite no encontrado para: {sprite_name}")
                # Crear sprite por defecto
                self.sprites[sprite_name] = self.create_default_sprite(sprite_name)
    
    def create_default_sprite(self, sprite_name):
        """Crea un sprite por defecto si no se encuentra el archivo"""
        if 'player' in sprite_name:
            surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            surface.fill(PLAYER_COLOR)
        elif 'enemy_circle' in sprite_name or 'boss_circle' in sprite_name:
            size = BOSS_SIZE if 'boss' in sprite_name else ENEMY_CIRCLE_SIZE
            surface = pygame.Surface((size, size))
            surface.fill(ENEMY_CIRCLE_COLOR)
        elif 'enemy_square' in sprite_name or 'boss_square' in sprite_name:
            size = BOSS_SIZE if 'boss' in sprite_name else ENEMY_SQUARE_SIZE
            surface = pygame.Surface((size, size))
            surface.fill(ENEMY_SQUARE_COLOR)
        elif 'enemy_triangle' in sprite_name or 'boss_triangle' in sprite_name:
            size = BOSS_SIZE if 'boss' in sprite_name else ENEMY_TRIANGLE_SIZE
            surface = pygame.Surface((size, size))
            surface.fill(ENEMY_TRIANGLE_COLOR)
        elif 'wall' in sprite_name:
            surface = pygame.Surface((WALL_THICKNESS, WALL_THICKNESS))
            surface.fill(GRAY)
        else:
            surface = pygame.Surface((50, 50))
            surface.fill((128, 128, 128))
        
        return surface
    
    def get_sprite(self, sprite_name):
        """Obtiene un sprite por nombre"""
        return self.sprites.get(sprite_name, self.create_default_sprite(sprite_name))
    
    def get_player_sprite(self):
        """Obtiene el sprite del jugador"""
        return self.get_sprite('player')
    
    def get_enemy_sprite(self, enemy_type, is_boss=False):
        """Obtiene el sprite de un enemigo"""
        if is_boss:
            return self.get_sprite(f'boss_{enemy_type}')
        else:
            return self.get_sprite(f'enemy_{enemy_type}')
    
    def get_wall_sprite(self):
        """Obtiene el sprite de una pared"""
        return self.get_sprite('wall')
    
    def get_background_sprite(self):
        """Obtiene el sprite de fondo"""
        return self.get_sprite('background')

# Instancia global del cargador de sprites
sprite_loader = SpriteLoader()

def load_sprite(sprite_name):
    """Función helper para cargar sprites"""
    return sprite_loader.get_sprite(sprite_name)
