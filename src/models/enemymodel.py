# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemymodel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:21:58 by rruiz           #+#    #+#               #
#  Updated: 2026/06/02 14:19:24 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

class EnemyModel:
   def __init__(self, mon: str, x: int, y: int, sprite_path: str, scale: int):
      self.start_pos = (x, y)
      self.x = x
      self.y = y
      self.sprite = arcade.Sprite(self.sprite, center_x=self.x, center_y=self.y, scale=1)