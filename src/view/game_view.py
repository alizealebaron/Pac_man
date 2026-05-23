# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rruiz <rruiz@student.42.fr>               +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 13:11:07 by alebaron        #+#    #+#               #
#  Updated: 2026/05/23 10:30:25 by rruiz           ###   ########.fr        #
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
        hexa_maze = self.manager.level[0].maze.maze
        self.maze_sprites: arcade.SpriteList = self._maze_to_draw(hexa_maze) 
        self.pacgums_sprites: arcade.SpriteList = self.put_pacgum(hexa_maze)

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.maze_sprites.draw()
        self.pacgums_sprites.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

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
        maze_width_size = nb_columns * 32
        nb_lines = len(rev_maze)
        maze_height_size = nb_lines * 32

        if self.window.width / maze_width_size > self.window.height / maze_height_size:
            self.scale = self.window.height / maze_height_size * 0.95
        else:
            self.scale = self.window.width / maze_width_size * 0.95
        self.offset_x  = (self.window.width - maze_width_size * self.scale) / 2
        self.offset_y = (self.window.height - maze_height_size * self.scale) / 2

        for line in wall_maze:
            for cell in line:
                for wall_path, x, y in cell:
                    center_x = (x - 0.5) * 32 * self.scale + self.offset_x
                    center_y = (y - 0.5) * 32 * self.scale + self.offset_y
                    sprite = arcade.Sprite(wall_path, center_x=center_x, center_y=center_y, scale=self.scale)
                    sprites.append(sprite)

        return sprites

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])
        
        return rev_maze

    def put_pacgum(self, maze: list[list[int]]) -> arcade.sprite_list:
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
                center_x = (x - 0.5) * 32 * self.scale + self.offset_x
                center_y = (y - 0.5) * 32 * self.scale + self.offset_y
                curr_coord = (x, y)
                if rev_maze[y - 1][x - 1] == 15 or (x, y) == center:
                    continue
                elif curr_coord in spacgum_coords:
                    sprite = arcade.Sprite(super_pacgum, center_x=center_x, center_y=center_y, scale=self.scale)
                else:
                    sprite = arcade.Sprite(pacgum, center_x=center_x, center_y=center_y, scale=self.scale)
                sprites.append(sprite)

        return sprites
