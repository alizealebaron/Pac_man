# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 13:11:07 by alebaron        #+#    #+#               #
#  Updated: 2026/05/29 18:02:40 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.view.maze_renderer import MazeRenderer
from src.managers.collectible_manager import CollectibleManager
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                 Global                                  |
# +-------------------------------------------------------------------------+

BACKGROUND_PATH = "assets/background/game_background.png"
MUSIC_PATH = "assets/music/game_theme.mp3"

SPEED = 10.0
TILE_SIZE = 64
TRANSITION_DISTANCE = 64

# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class GameView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, manager: PacmanManager):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Récupération de la hauteur et de la largeur
        self.largeur = self.window.width
        self.hauteur = self.window.height

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

        # Récupération du manager et du labyrinthe
        self.manager = manager
        self.current_maze = self.manager.level[0].maze.maze

        # Récupération du labyrinthe à l'envers pour Arcade
        self.rev_maze = self._rev_maze(self.current_maze)

        # Initialiser les renderers
        self.maze_renderer = MazeRenderer(self.rev_maze, self.largeur, self.hauteur)
        self.scale = self.maze_renderer.scale
        self.offset_x, self.offset_y = self.maze_renderer.offset_x, self.maze_renderer.offset_y

        # Initialisation du gestionnaire de collectibles
        self.collectible_manager = CollectibleManager(self.rev_maze, self.scale, self.offset_x, self.offset_y)

        # Initialisation des coords du player et de ces sprites
        self._player_original_pos()
        self.player_sprite = arcade.Sprite('assets/sprite/rond_de_merde.png', scale=self.scale)
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        # Music
        self.music_player = None

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Draw everything """
        self.clear()

        # Affichage du background
        self.draw_background()

        # Affichage du labyrinthe et des pacgums
        self.maze_renderer.draw()
        self.collectible_manager.draw()

        # Récupération des coordonnées du joueur en pixel
        pixel_x = self.manager.player.x * TILE_SIZE + 32 + self.manager.player.pixel_offset_x
        pixel_y = self.manager.player.y * TILE_SIZE + 32 + self.manager.player.pixel_offset_y

        # Affichage du joueur au centre du labyrinthe
        self.player_sprite.center_x = pixel_x * self.scale + self.offset_x
        self.player_sprite.center_y = pixel_y * self.scale + self.offset_y
        self.player_sprites.draw()

        # Affichage de l'HUD
        self.draw_UHD()

    def on_update(self, delta_time):
        """ Movement and game logic """
        vx, vy = self._player_move()

        self.manager.player.pixel_offset_x += vx * SPEED
        self.manager.player.pixel_offset_y += vy * SPEED

        if self.manager.player.pixel_offset_x >= TRANSITION_DISTANCE:
            self.manager.player.x += 1
            self.manager.player.pixel_offset_x = 0
        elif self.manager.player.pixel_offset_x <= -TRANSITION_DISTANCE:
            self.manager.player.x -= 1
            self.manager.player.pixel_offset_x = 0
        
        if self.manager.player.pixel_offset_y >= TRANSITION_DISTANCE:
            self.manager.player.y += 1
            self.manager.player.pixel_offset_y = 0
        elif self.manager.player.pixel_offset_y <= -TRANSITION_DISTANCE:
            self.manager.player.y -= 1
            self.manager.player.pixel_offset_y = 0

    def on_show_view(self):
        """Appelé quand la vue change"""
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=1, loop=True)

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])

        return rev_maze

    def _player_original_pos(self):
        nb_columns = len(self.rev_maze[0])
        nb_lines = len(self.rev_maze)

        grid_x = (nb_columns) // 2 if nb_columns % 2 == 0 else (nb_columns + 1) // 2
        grid_y = (nb_lines) // 2 + 1 if nb_lines % 2 == 0 else (nb_lines + 1) // 2

        self.manager.player.x = grid_x - 1
        self.manager.player.y = grid_y - 1

        self.manager.player.pixel_offset_x = 0.0
        self.manager.player.pixel_offset_y = 0.0

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case arcade.key.UP:
                self.manager.player.next_direction = "up"
            case arcade.key.LEFT:
                self.manager.player.next_direction = "left"
            case arcade.key.DOWN:
                self.manager.player.next_direction = "down"
            case arcade.key.RIGHT:
                self.manager.player.next_direction = "right"

        match symbol:
            case arcade.key.W:
                self.manager.player.next_direction = "up"
            case arcade.key.A:
                self.manager.player.next_direction = "left"
            case arcade.key.S:
                self.manager.player.next_direction = "down"
            case arcade.key.D:
                self.manager.player.next_direction = "right"

    def _player_move(self) -> tuple[float, float]:
        player = self.manager.player

        if player.next_direction and self._is_opposite_direction(player.direction, player.next_direction):
            player.direction = player.next_direction
            player.next_direction = None

        elif player.pixel_offset_x == 0 and player.pixel_offset_y == 0:
            if player.next_direction and self._can_move(player.next_direction):
                player.direction = player.next_direction
                player.next_direction = None

        if player.direction and self._can_move(player.direction):
            match player.direction:
                case "up":
                    return (0, 1)
                case "right":
                    return (1, 0)
                case "down":
                    return (0, -1)
                case "left":
                    return (-1, 0)
                case _:
                    return (0, 0)
        else:
            return (0, 0)

    def _can_move(self, direction: str) -> bool:
        grid_x = self.manager.player.x
        grid_y = self.manager.player.y
        if grid_y < 0 or grid_y >= len(self.rev_maze) or grid_x < 0 or grid_x >= len(self.rev_maze[0]):
            return False

        match direction:
            case "up":
                if not (self.rev_maze[grid_y][grid_x] & 1):
                    return True
            case "right":
                if not (self.rev_maze[grid_y][grid_x] & 2):
                    return True
            case "down":
                if not (self.rev_maze[grid_y][grid_x] & 4):
                    return True
            case "left":
                if not (self.rev_maze[grid_y][grid_x] & 8):
                    if self.offset_x != 0:
                        return True
                    return True
            case _:
                return False

    def _is_opposite_direction(self, current: str, next_dir: str) -> bool:
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        return opposites.get(current) == next_dir


    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_background(self):

        background = arcade.load_texture(BACKGROUND_PATH)
        arcade.draw_texture_rect(
            texture=background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

    def draw_UHD(self):

        pokemon = self.manager.player.pokemon
        sprite = arcade.load_texture(f"assets/sprite/pokemon/{pokemon}"
                                     "/portraits/Normal.png")
        sprite_size = 75

        arcade.draw_texture_rect(
            texture=sprite,
            rect=arcade.XYWH((sprite_size / 2) + 10,
                             (self.hauteur - (sprite_size / 2) - 10),
                             sprite_size,
                             sprite_size)
        )

        sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        arcade.draw_texture_rect(
            texture=sprite_frame,
            rect=arcade.XYWH((sprite_size / 2) + 10,
                             (self.hauteur - (sprite_size / 2) - 10),
                             sprite_size + 9,
                             sprite_size + 9)
        )

        player_life = arcade.Text(f"Live(s): {self.manager.player.nb_life}",
                                  sprite_size + 25,
                                  (self.hauteur - (sprite_size / 2) - 5),
                                  color=arcade.color.BLACK,
                                  font_size=15,
                                  font_name="Comic Sans MS")
        player_life.draw()

        player_life = arcade.Text(f"Score: {self.manager.player.score}",
                                  sprite_size + 25,
                                  (self.hauteur - (sprite_size / 2) - 35),
                                  color=arcade.color.BLACK,
                                  font_size=15,
                                  font_name="Comic Sans MS")
        player_life.draw()
