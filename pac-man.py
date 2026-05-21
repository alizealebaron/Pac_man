# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 16:14:42 by alebaron        #+#    #+#               #
#  Updated: 2026/05/21 11:43:12 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import time
import arcade
import argparse
import sys
from src.parsing.arg_parser import check_argument
from src.parsing.config_loader import ConfigLoader
from src.view.main_window import MainWindow
from src.view.menu_view import MenuView
from src.models.configmodel import ConfigModel
from src.score.score_file import retrieve_score_from_json

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pacmon Mystery Dungeon"
SCORE_FILE = "data/score.json"

# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+


def main() -> None:

    try:
        # Récupération de la config
        arg: argparse.Namespace = check_argument()
        config: ConfigModel = ConfigLoader.load_config(arg.config_file)

        # Récupération du scoreboard
        scoreboard = retrieve_score_from_json(SCORE_FILE)

        # Affichage de la fenêtre de début de jeu

        window = MainWindow(title=SCREEN_TITLE, fullscreen=True,
                            score=scoreboard, config=config)
        arcade.run()

    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
