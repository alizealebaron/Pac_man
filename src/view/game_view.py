# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rruiz <rruiz@student.42.fr>               +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 13:11:07 by alebaron        #+#    #+#               #
#  Updated: 2026/05/22 14:45:16 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.view.gameover_view import GameoverView
from src.pacmanManager import PacmanManager


square_wall = 'assets/sprite/wall/A.png'
east_wall = 'assets/sprite/wall/E.png'
north_wall = 'assets/sprite/wall/N.png'
west_wall = 'assets/sprite/wall/O.png'
south_wall = 'assets/sprite/wall/S.png'

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
        # self.window.set_mouse_visible(False)

        # arcade.set_background_color(arcade.color.AMAZON)
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = manager
        hexa_maze = self.manager.level[0].maze.maze
        self.maze_sprites: arcade.SpriteList = self._maze_to_draw(hexa_maze)

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Draw everything """
        self.clear()
        # arcade.draw_text("Game view", self.window.width / 2, self.window.height / 2,
        #                  arcade.color.WHITE, font_size=50, anchor_x="center")
        self.maze_sprites.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

    def _maze_to_draw(self, maze) -> arcade.SpriteList:
        sprites = arcade.SpriteList()

        for test in (square_wall, east_wall, north_wall, west_wall, south_wall):
            test2 = arcade.Sprite(test)
            tile_size = test2.width
            print(f"Taille réelle de {test} : {tile_size}px")

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
                line_maze.append(wall)
            wall_maze.append(line_maze)

        nb_columns = len(rev_maze[0])
        maze_width_size = nb_columns * 32
        nb_lines = len(rev_maze)
        maze_height_size = nb_lines * 32

        if self.window.width / maze_width_size > self.window.height / maze_height_size:
            scale = self.window.height / maze_height_size * 0.95
        else:
            scale = self.window.width / maze_width_size * 0.95
        offset_x  = (self.window.width - maze_width_size * scale) / 2
        offset_y = (self.window.height - maze_height_size * scale) / 2

        print(f"window: {self.window.width}x{self.window.height}")
        print(f"maze: {nb_columns}x{nb_lines} tiles → {maze_width_size}x{maze_height_size}px")
        print(f"scale: {scale}")
        print(f"offset: x={offset_x}, y={offset_y}")
        print(f"premier sprite y = {(1 - 0.5) * 32 * scale + offset_y}")
        print(f"dernier sprite y = {(nb_lines - 0.5) * 32 * scale + offset_y}")
        print(f"hauteur fenetre = {self.window.height}")

        for line in wall_maze:
            for cell in line:
                for wall_path, x, y in cell:
                    center_x = (x - 0.5) * 32 * scale + offset_x
                    center_y = (y - 0.5) * 32 * scale + offset_y
                    sprite = arcade.Sprite(wall_path, center_x=center_x, center_y=center_y, scale=scale)
                    sprites.append(sprite)

        return sprites

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])
        
        return rev_maze
