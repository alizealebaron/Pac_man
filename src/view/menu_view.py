# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 10:28:01 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 16:20:01 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import arcade.gui
from src.view.game_view import GameView

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/background.jpg"
BTN_PATH = "assets/button/"

# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class MenuView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):

        super().__init__()

        # Initialisation du background
        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation de la box à boutons
        self.boutons = {
            "start": {
                "texture": arcade.load_texture(BTN_PATH + "start.png"),
                "pos": (800, 800),
                "action": self.demarrer_jeu
            },
            "quizz": {
                "texture": arcade.load_texture(BTN_PATH + "quizz.png"),
                "pos": (500, 500),
                "action": None
            },
            "settings": {
                "texture": arcade.load_texture(BTN_PATH + "settings.png"),
                "pos": (500, 500),
                "action": None
            },
            "exit": {
                "texture": arcade.load_texture(BTN_PATH + "end.png"),
                "pos": (500, 500),
                "action": self.quitter_jeu
            }
        }

    def demarrer_jeu(self):
        print("Lancement du jeu...")
        self.window.show_view(GameView())

    def quitter_jeu(self):
        arcade.exit()

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

        for nom, data in self.boutons.items():
            # On dessine chaque bouton dynamiquement
            arcade.draw_texture_rect(
                texture=data["texture"],
                rect=arcade.XYWH(data["pos"][0], data["pos"][1], 400, 250)
            )

    def on_mouse_press(self, x, y, button, modifiers):
        for nom, data in self.boutons.items():
            bx, by = data["pos"]
            # Vérification simple de collision (ici pour un bouton de 200x50)
            if bx - 200 < x < bx + 200 and by - 125 < y < by + 125:
                data["action"]()
