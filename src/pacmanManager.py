# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacmanManager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rruiz <rruiz@student.42.fr>               +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 13:04:41 by alebaron        #+#    #+#               #
#  Updated: 2026/05/22 12:04:10 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import argparse
import json
from src.parsing.config_loader import ConfigLoader
from src.models.configmodel import ConfigModel, LevelConfig
from src.models.scoreModel import Score
from src.models.playerModel import PlayerModel
from src.models.levelModel import Level

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

        # Generation des maps et stockage dans une liste
        self.level: list[Level] = self.create_maps(self.config.level)

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


    def create_maps(self, level: list[LevelConfig]) -> list[Level]:
        level_list: list[Level] = []
        for map in level:
            level_list.append(Level(map.id, map.width, map.height))
        return level_list
