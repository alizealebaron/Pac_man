# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 14:35:28 by alebaron        #+#    #+#               #
#  Updated: 2026/05/21 13:10:24 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.models.scoreModel import Score
from src.models.configmodel import ConfigModel
from src.view.menu_view import MenuView
from src.pacmanManager import PacmanManager


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class MainWindow(arcade.Window):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, title: str, fullscreen: bool, manager: PacmanManager):

        super().__init__(title=title, fullscreen=fullscreen)
        self.pacman = manager

        # Démarrer le jeu
        start_view = MenuView()
        self.show_view(start_view)
