# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemy_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:41:40 by rruiz           #+#    #+#               #
#  Updated: 2026/06/02 14:19:43 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from src.models.configmodel import ConfigModel
from src.models.enemymodel import EnemyModel

blinky = 'Drifloon'
clyde = 'Duskull'
inky = 'Haunter'
pinky = 'Misdreavus'

class EnemyManager:
    def __init__(self, config: ConfigModel, curr_level: list[list[int]]):
        self.config = config
        self.level = curr_level
        self.enemies: list[EnemyModel] = self._create_enemies()


    def _create_enemies(self) -> list[EnemyModel]:
        width = self.level.maze._width
        height = self.level.maze._height
        enemies = [(blinky, 0, 0), (clyde, 0, height), (inky, width, 0), (pinky, width, height)]

        for mon, x, y in enemies:
            sprite = 'assets/sprite/inky_de_merde.png'
            # sprite = f'assets/sprite/enemy/{mon}/animations/Walk-Anim.png'
            scale = 1
            enemy = EnemyModel(mon, x, y, sprite, scale)
            self.enemies.append(enemy)