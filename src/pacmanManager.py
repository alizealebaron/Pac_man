# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacmanManager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 13:04:41 by alebaron        #+#    #+#               #
#  Updated: 2026/05/21 16:10:26 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import argparse
import json
from src.parsing.config_loader import ConfigLoader
from src.models.configmodel import ConfigModel
from src.models.scoreModel import Score
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
        self.scoreboard = self.retrieve_score_from_json()

        # Génération aléatoire du joueur
        self.player = PlayerModel()

    # +---------------------------------------------------------------------+
    # |                            JSON Methods                             |
    # +---------------------------------------------------------------------+

    def retrieve_score_from_json(self):

        lst_score = []

        try:
            with open(SCORE_FILE, "r") as file:
                data = json.load(file)
                lst_score = [Score(**arg) for arg in data]
        except json.JSONDecodeError as e:
            raise (e)
        except Exception:
            pass

        return lst_score

    def update_json_score(self):

        dict_data = [obj.__dict__ for obj in self.scoreboard]

        with open(SCORE_FILE, "w") as f:
            json.dump(dict_data, f, indent=2)
