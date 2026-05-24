# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  playerModel.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 12:46:42 by alebaron        #+#    #+#               #
#  Updated: 2026/05/24 19:58:31 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import os
import random
import arcade
from src.models.configmodel import ConfigModel


# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+

POKEMON_PATH = "assets/sprite/pokemon"

# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PlayerModel():

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, config: ConfigModel):

        self.pokemon = self._get_random_pokemon()
        self.name = self._get_random_name()
        self.x = 0
        self.y = 0
        self.direction = None
        self.sprite = arcade.Sprite('assets/sprite/petit_fantom.png')
        self.nb_life = config.lives
        self.score = 0

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def _get_random_pokemon(self):

        return (random.choice(os.listdir(POKEMON_PATH)))

    def _get_random_name(self):

        prefixe = ["Bold", "Quirky", "Brave", "Calm", "Quiet", "Docile",
                   "Mild", "Rash", "Gentle", "Hardy", "Jolly", "Lax",
                   "Impish", "Sassy", "Naughty", "Modest", "Naive", "Hasty",
                   "Careful", "Bashful", "Relaxed", "Adamant", "Serious",
                   "Lonely", "Timid", "Chaotic"]

        return random.choice(prefixe) + "_" + self.pokemon
