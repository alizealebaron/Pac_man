# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rruiz <rruiz@student.42.fr>               +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 13:11:07 by alebaron        #+#    #+#               #
#  Updated: 2026/05/22 09:44:48 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.view.gameover_view import GameoverView


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

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        # arcade.set_background_color(arcade.color.AMAZON)
        arcade.set_background_color(arcade.color.BLACK)

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Draw everything """
        self.clear()
        # arcade.draw_text("Game view", self.window.width / 2, self.window.height / 2,
        #                  arcade.color.WHITE, font_size=50, anchor_x="center")
        test = [[13, 1, 1, 1, 1, 5, 1, 3, 9, 1, 1, 5, 5, 1, 1, 5, 1, 3, 9, 7],
        [9, 6, 12, 4, 2, 9, 2, 8, 2, 10, 12, 1, 1, 4, 6, 9, 6, 10, 8, 3],
        [12, 3, 9, 5, 6, 8, 2, 12, 4, 2, 9, 4, 6, 13, 1, 4, 1, 2, 10, 10],
        [11, 10, 8, 5, 1, 6, 12, 5, 5, 6, 8, 3, 9, 1, 4, 1, 4, 2, 10, 10],
        [8, 2, 10, 9, 4, 1, 5, 3, 9, 1, 4, 2, 10, 8, 5, 0, 5, 2, 10, 10],
        [10, 10, 12, 6, 9, 6, 9, 2, 10, 8, 3, 12, 4, 2, 9, 4, 1, 2, 10, 10],
        [10, 12, 1, 1, 4, 1, 6, 12, 6, 10, 12, 5, 5, 6, 8, 5, 4, 4, 4, 2],
        [12, 3, 8, 4, 5, 6, 15, 9, 5, 2, 15, 15, 15, 9, 4, 1, 5, 1, 5, 2],
        [11, 12, 6, 9, 1, 3, 15, 12, 7, 8, 5, 7, 15, 8, 7, 12, 5, 6, 9, 6],
        [10, 9, 5, 4, 2, 10, 15, 15, 15, 10, 15, 15, 15, 10, 9, 3, 9, 1, 6, 11],
        [8, 4, 1, 5, 2, 8, 5, 3, 15, 10, 15, 13, 5, 2, 10, 12, 6, 8, 1, 2],
        [10, 11, 10, 13, 6, 10, 9, 6, 15, 10, 15, 15, 15, 10, 10, 9, 1, 6, 10, 10],
        [12, 2, 10, 9, 1, 2, 12, 1, 1, 4, 1, 5, 3, 8, 4, 6, 8, 3, 8, 6],
        [9, 2, 8, 4, 2, 12, 1, 2, 12, 1, 4, 1, 2, 12, 5, 5, 4, 4, 2, 11],
        [10, 12, 0, 7, 12, 1, 6, 12, 5, 6, 9, 2, 12, 1, 1, 3, 9, 1, 2, 10],
        [8, 3, 14, 9, 1, 4, 3, 9, 5, 5, 6, 8, 3, 10, 8, 4, 4, 2, 12, 2],
        [10, 8, 1, 6, 10, 11, 8, 4, 1, 3, 9, 2, 12, 2, 8, 1, 1, 2, 11, 10],
        [10, 12, 4, 3, 8, 2, 10, 11, 8, 6, 10, 8, 1, 2, 8, 4, 4, 4, 4, 2],
        [8, 1, 1, 2, 8, 4, 0, 6, 12, 1, 2, 10, 8, 4, 4, 7, 9, 5, 5, 2],
        [12, 4, 4, 6, 12, 5, 4, 5, 5, 4, 6, 12, 4, 5, 5, 5, 4, 5, 5, 6]]

        sprites = arcade.SpriteList()

        maze: list[list[int]] = self._rev_maze(test)
        wall_maze = []
        y = 0
        for line in maze:
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

        for line in wall_maze:
            for cell in line:
                for wall_path, x, y in cell:
                    sprite = arcade.Sprite(wall_path, center_x=x*32, center_y=y*32, scale=1)
                    sprites.append(sprite)

        sprites.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])
        
        return rev_maze
