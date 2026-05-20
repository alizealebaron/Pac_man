# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 16:14:42 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 16:59:14 by alebaron        ###   ########.fr        #
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
from src.view.menu_view import MenuView
from src.view.gameover_view import GameoverView
from src.models.configmodel import ConfigModel

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pacmon Mystery Dungeon"


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+


def main() -> None:
    try:
        arg: argparse.Namespace = check_argument()
        config: ConfigModel = ConfigLoader.load_config(arg.config_file)

        # Affichage de la fenêtre de début de jeu

        window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        menu_view = MenuView()
        window.show_view(menu_view)
        arcade.run()

    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
