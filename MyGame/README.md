# MAZE HUNT

Un juego de laberinto desarrollado en Python usando Pygame.

## Descripción del Juego

MAZE HUNT es un juego donde el jugador debe escapar de enemigos en un laberinto. El juego cuenta con 9 niveles, cada uno con un diseño de laberinto único. Cada 3 niveles hay un nivel especial con un jefe.

### Mecánicas del Juego

- **Jugador**: Representado por un cuadrado azul que se mueve con las teclas WASD o flechas
- **Enemigos**: Tres tipos diferentes:
  - **Círculos rojos**: Enemigos básicos
  - **Cuadrados verdes**: Enemigos con habilidades especiales
  - **Triángulos amarillos**: Enemigos rápidos
- **Modo Caza**: Cada minuto se activa un temporizador donde:
  - El jugador puede matar enemigos si los atrapa
  - Los enemigos se vuelven más lentos
  - Los enemigos se reúnen en una esquina para ser más fuertes
  - El temporizador principal se pausa
- **Jefes**: En los niveles 3, 6 y 9 hay jefes especiales más grandes y fuertes
- **Objetivo**: Matar a todos los enemigos en 5 minutos (sin contar el tiempo de caza)

## Instalación

1. Asegúrate de tener Python 3.6 o superior instalado
2. Instala Pygame:
   ```bash
   pip install pygame
   ```
3. Ejecuta el juego:
   ```bash
   python main.py
   ```

## Estructura del Proyecto

```
MyGame/
├── main.py          # Archivo principal del juego
├── lobby.py         # Pantalla de inicio
├── levels.py        # Selección de niveles
├── options.py       # Configuración del juego
├── sprites.py       # Clases de personajes y enemigos
├── settings.py      # Configuraciones del juego
├── audio.py         # Gestión de audio
├── assets/
│   ├── Sounds/      # Archivos de audio
│   └── Imagen/      # Archivos de imagen
└── README.md        # Este archivo
```

## Controles

- **WASD** o **Flechas**: Mover el jugador
- **Mouse**: Navegar por los menús
- **Click**: Seleccionar botones

## Características

### Pantalla Principal (Lobby)
- Título "MAZE HUNT" con efecto pixelado
- Botón PLAY para acceder a los niveles
- Botón OPTIONS para configurar el juego

### Selección de Niveles
- 9 niveles organizados en una cuadrícula 3x3
- Niveles de jefe marcados especialmente
- Botón BACK para volver al lobby

### Opciones
- Control de volumen maestro
- Control de volumen de música
- Control de volumen de efectos de sonido
- Control de brillo
- Botón para resetear a valores por defecto

### Audio
- Música de fondo para cada sección
- Efectos de sonido para interacciones
- Sonidos especiales para el modo caza
- Efectos de muerte y otros eventos

## Niveles

1. **Nivel 1**: Tutorial básico
2. **Nivel 2**: Complejidad media
3. **Nivel 3**: Jefe Círculo
4. **Nivel 4**: Laberinto más complejo
5. **Nivel 5**: Enemigos adicionales
6. **Nivel 6**: Jefe Cuadrado
7. **Nivel 7**: Mecánicas avanzadas
8. **Nivel 8**: Preparación para jefe final
9. **Nivel 9**: Jefe Triángulo (Final)

## Personalización

Puedes modificar las configuraciones en `settings.py`:
- Tamaños de pantalla
- Velocidades de personajes
- Colores
- Tiempos de juego
- Configuraciones de audio

## Requisitos del Sistema

- Python 3.6+
- Pygame 2.0+
- Sistema operativo: Windows, macOS, o Linux

## Desarrollo

Para contribuir al desarrollo:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Envía un pull request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Contacto

Para preguntas o sugerencias, contacta al desarrollador.

---

¡Disfruta jugando MAZE HUNT!
