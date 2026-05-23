# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rruiz <rruiz@student.42.fr>               +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 13:11:07 by alebaron        #+#    #+#               #
#  Updated: 2026/05/27 14:49:51 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.view.gameover_view import GameoverView
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                 Global                                  |
# +-------------------------------------------------------------------------+

square_wall = 'assets/sprite/wall/A.png'
east_wall = 'assets/sprite/wall/E.png'
north_wall = 'assets/sprite/wall/N.png'
west_wall = 'assets/sprite/wall/O.png'
south_wall = 'assets/sprite/wall/S.png'

pacgum = 'assets/sprite/collectible/pacgum.png'
super_pacgum = 'assets/sprite/collectible/super_pacgum.png'

BACKGROUND_PATH = "assets/background/game_background.png"
MUSIC_PATH = "assets/music/game_theme.mp3"

# +-    ------------------------------------------------------------------------+
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

        self.manager = manager
        self.maze_sprites: arcade.SpriteList = self._maze_to_draw(self.manager.level[0].maze.maze) 
        self.pacgums_sprites: arcade.SpriteList = self._put_pacgum(self.manager.level[0].maze.maze)

        self._player_original_pos(self.manager.level[0].maze.maze)
        self.player_sprite = arcade.Sprite('assets/sprite/petit_fantom.png', center_x=self.manager.player.x, center_y=self.manager.player.y, scale=self.scale)
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        self.move_timer = 0
        self.sprite_x = (self.manager.player.x - 0.5) * 64 * self.scale + self.offset_x
        self.sprite_y = (self.manager.player.y - 0.5) * 64 * self.scale + self.offset_y

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

        self.maze_sprites.draw()
        self.pacgums_sprites.draw()
        self.player_sprites.draw()

        # Affichage de l'UHD
        self.draw_UHD()

    def on_update(self, delta_time):
        """ Movement and game logic """
        target_x = (self.manager.player.x - 0.5) * 64 * self.scale + self.offset_x
        target_y = (self.manager.player.y - 0.5) * 64 * self.scale + self.offset_y

        arrived = abs(target_x - self.sprite_x) < 1 and abs(target_y - self.sprite_y) < 1

        if arrived:
            self.manager.player.direction = self.manager.player.next_direction

        self.move_timer += delta_time
        if self.move_timer > 0.1 and arrived:
            self._player_move()
            self.move_timer = 0

        speed = 10
        self.sprite_x += (target_x - self.sprite_x) * speed * delta_time
        self.sprite_y += (target_y - self.sprite_y) * speed * delta_time
        self.player_sprite.center_x = self.sprite_x
        self.player_sprite.center_y = self.sprite_y

    def on_show_view(self):
        """Appelé quand la vue change"""
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=1, loop=True)

    def _maze_to_draw(self, maze: list[list[int]]) -> arcade.SpriteList:
        sprites = arcade.SpriteList()

        rev_maze: list[list[int]] = self._rev_maze(maze)
        wall_maze = []
        y = 0
        for line in rev_maze:
            y += 1
            x = 0
            line_maze = []
            for value in line:
                x += 1
                wall = []
                if value & 1:
                    wall.append((north_wall, x, y))
                if value & 2:
                    wall.append((east_wall, x, y))
                if value & 4:
                    wall.append((south_wall, x, y))
                if value & 8:
                    wall.append((west_wall, x, y))
                if len(wall) == 4:
                    wall = [(square_wall, x, y)]
                line_maze.append(wall)
            wall_maze.append(line_maze)

        nb_columns = len(rev_maze[0])
        maze_width_size = nb_columns * 64
        nb_lines = len(rev_maze)
        maze_height_size = nb_lines * 64

        if self.window.width / maze_width_size > self.window.height / maze_height_size:
            self.scale = self.window.height / maze_height_size * 0.95
        else:
            self.scale = self.window.width / maze_width_size * 0.95
        self.offset_x  = (self.window.width - maze_width_size * self.scale) / 2
        self.offset_y = (self.window.height - maze_height_size * self.scale) / 2

        for line in wall_maze:
            for cell in line:
                for wall_path, x, y in cell:
                    center_x = (x - 0.5) * 64 * self.scale + self.offset_x
                    center_y = (y - 0.5) * 64 * self.scale + self.offset_y
                    sprite = arcade.Sprite(wall_path, center_x=center_x, center_y=center_y, scale=self.scale)
                    sprites.append(sprite)

        return sprites

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])
        
        return rev_maze

    def _put_pacgum(self, maze: list[list[int]]) -> arcade.sprite_list:
        sprites = arcade.SpriteList()
        rev_maze = self._rev_maze(maze)
 
        nb_columns = len(rev_maze[0])
        nb_lines = len(rev_maze)

        spacgum_coords = [(1, 1), (1, nb_lines), (nb_columns, 1),
                         (nb_columns, nb_lines)]

        x_center = (nb_columns ) // 2 if nb_columns % 2 == 0 else (nb_columns + 1) // 2
        y_center = (nb_lines) // 2 + 1 if nb_lines % 2 == 0 else (nb_lines + 1) // 2
        center = x_center, y_center

        for y in range(1, nb_lines + 1):
            for x in range(1, nb_columns + 1):
                center_x = (x - 0.5) * 64 * self.scale + self.offset_x
                center_y = (y - 0.5) * 64 * self.scale + self.offset_y
                curr_coord = (x, y)
                if rev_maze[y - 1][x - 1] == 15 or (x, y) == center:
                    continue
                elif curr_coord in spacgum_coords:
                    sprite = arcade.Sprite(super_pacgum, center_x=center_x, center_y=center_y, scale=self.scale)
                else:
                    sprite = arcade.Sprite(pacgum, center_x=center_x, center_y=center_y, scale=self.scale)
                sprites.append(sprite)

        return sprites

    def _player_original_pos(self, maze: list[list[int]]):
        rev_maze = self._rev_maze(maze)

        nb_columns = len(rev_maze[0])
        nb_lines = len(rev_maze)

        self.manager.player.x = (nb_columns ) // 2 if nb_columns % 2 == 0 else (nb_columns + 1) // 2
        self.manager.player.y = (nb_lines) // 2 + 1 if nb_lines % 2 == 0 else (nb_lines + 1) // 2

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

    def _player_move(self):
        maze = self.manager.level[0].maze.maze
        rev_maze = self._rev_maze(maze)
        player = self.manager.player

        new_x = player.x
        new_y = player.y

        match player.direction:
            case "up":
                if not (rev_maze[new_y - 1][new_x - 1] & 1):
                    new_y += 1
            case "right":
                if not (rev_maze[new_y - 1][new_x - 1] & 2):
                    new_x += 1
            case "down":
                if not (rev_maze[new_y - 1][new_x - 1] & 4):
                    new_y -= 1
            case "left":
                if not rev_maze[new_y - 1][new_x - 1] & 8:
                    new_x -= 1

        nb_columns = len(rev_maze[0])
        nb_lines = len(rev_maze)

        if 1 <= new_x <= nb_columns:
            player.x = new_x

        if 1 <= new_y <= nb_lines:
            player.y = new_y

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