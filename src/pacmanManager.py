# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacmanManager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 13:04:41 by alebaron        #+#    #+#               #
#  Updated: 2026/05/21 13:09:31 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import argparse
from src.parsing.config_loader import ConfigLoader
from src.models.configmodel import ConfigModel
from src.score.score_file import retrieve_score_from_json
from src.models.playerModel import PlayerModel

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


SCORE_FILE = "data/score.json"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PacmanManager():

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, arg: argparse.Namespace):

        # Récupération de la config
        self.config: ConfigModel = ConfigLoader.load_config(arg.config_file)

        # Récupération du scoreboard
        self.scoreboard = retrieve_score_from_json(SCORE_FILE)

        # Génération aléatoire du joueur
        self.player = PlayerModel()
