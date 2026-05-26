# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rruiz <rruiz@student.42.fr>               +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 13:11:07 by alebaron        #+#    #+#               #
#  Updated: 2026/05/26 05:23:07 by rruiz           ###   ########.fr        #
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

SPEED = 2

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

        self.display_x = (self.manager.player.x - 0.5) * 64 * self.scale + self.offset_x
        self.display_y = (self.manager.player.y - 0.5) * 64 * self.scale + self.offset_y

        self.is_moving = False
        self.move_progress = 0.0
        self.is_start = True

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.maze_sprites.draw()
        self.pacgums_sprites.draw()
        self.player_sprites.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        old_x = self.manager.player.x
        old_y = self.manager.player.y
        self._player_move()

        if self.is_start:
            self.player_sprite.center_x = self.display_x
            self.player_sprite.center_y = self.display_y
            self.is_start = False

        if old_x != self.manager.player.x or old_y != self.manager.player.y:
            self.is_moving = True
            self.current_x = self.player_sprite.center_x
            self.current_y = self.player_sprite.center_y
            self.target_x, self.target_y = self.grid_to_screen(self.manager.player.x, self.manager.player.y)
            self.move_progress = 0
        
        if self.is_moving:
            self.move_progress += delta_time * SPEED
            if self.move_progress >= 1.0:
                self.is_moving = False
                self.player_sprite.center_x = self.target_x
                self.player_sprite.center_y = self.target_y
                self.move_progress = 1.0
            else:
                self.player_sprite.center_x = self.current_x + (self.target_x - self.current_x) * self.move_progress
                self.player_sprite.center_y = self.current_y + (self.target_y - self.current_y) * self.move_progress


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
                self.manager.player.direction = "up"
            case arcade.key.LEFT:
                self.manager.player.direction = "left"
            case arcade.key.DOWN:
                self.manager.player.direction = "down"
            case arcade.key.RIGHT:
                self.manager.player.direction = "right"

        match symbol:
            case arcade.key.W:
                self.manager.player.direction = "up"
            case arcade.key.A:
                self.manager.player.direction = "left"
            case arcade.key.S:
                self.manager.player.direction = "down"
            case arcade.key.D:
                self.manager.player.direction = "right"

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

    def grid_to_screen(self, grid_x, grid_y):
        screen_x = (grid_x - 0.5) * 64 * self.scale + self.offset_x
        screen_y = (grid_y - 0.5) * 64 * self.scale + self.offset_y
        return (screen_x, screen_y)