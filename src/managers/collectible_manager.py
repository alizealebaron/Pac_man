# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collectible_manager.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/28 16:43:54 by rruiz           #+#    #+#               #
#  Updated: 2026/05/29 09:51:02 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

PACGUM_PATH = 'assets/sprite/collectible/pacgum.png'
SUPER_PACGUM_PATH = 'assets/sprite/collectible/super_pacgum.png'
TILE_SIZE = 64

class CollectibleManager:
    """Gère le placement et l'affichage des pacgums"""

    def __init__(self, maze: list[list[int]], scale: float = 1.0, offset_x: float = 0.0, offset_y: float = 0.0):
        self.maze = maze
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.sprites = arcade.SpriteList()

        # Initialiser les pacgums
        self._place_collectibles()

    def _place_collectibles(self):
        nb_columns = len(self.maze[0])
        nb_lines = len(self.maze)

        # Super pacgums dans les coins
        super_pacgum_coords = [(1, 1), (1, nb_lines), (nb_columns, 1),
                               (nb_columns, nb_lines)]

        # Pas de pacgum au centre du maze
        x_center = (nb_columns) // 2 if nb_columns % 2 == 0 else (nb_columns + 1) // 2
        y_center = (nb_lines) // 2 + 1 if nb_lines % 2 == 0 else (nb_lines + 1) // 2
        center = (x_center, y_center)

        for y in range(1, nb_lines + 1):
            for x in range(1, nb_columns + 1):
                curr_coord = (x, y)
                if self.maze[y - 1][x - 1] == 15 or curr_coord == center:
                    continue
                center_x = (x - 0.5) * TILE_SIZE * self.scale + self.offset_x
                center_y = (y - 0.5) * TILE_SIZE * self.scale + self.offset_y

                if curr_coord in super_pacgum_coords:
                    sprite = arcade.Sprite(SUPER_PACGUM_PATH, center_x=center_x, center_y=center_y, scale=self.scale)
                else:
                    sprite = arcade.Sprite(PACGUM_PATH, center_x=center_x, center_y=center_y, scale=self.scale)

                self.sprites.append(sprite)

    def draw(self):
        """ Draw everything """
        self.sprites.draw()
