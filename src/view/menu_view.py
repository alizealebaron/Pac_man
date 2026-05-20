# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 10:28:01 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 21:11:26 by alebaron        ###   ########.fr        #
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

        # Récupération de la largeur et hauteur de la fenêtre
        largeur = self.window.width
        hauteur = self.window.height

        # Calcul des dimensions proportionnelles des boutons
        self.btn_width = largeur * 0.20
        self.btn_height = hauteur * 0.17

        # Calcul des positions (en % de l'écran)
        col_gauche = largeur * 0.35
        col_droite = largeur * 0.65
        col_centre = largeur * 0.50

        ligne_haut = hauteur * 0.75
        ligne_milieu = hauteur * 0.48
        ligne_bas = hauteur * 0.20

        # Initialisation de la box à boutons
        self.boutons = {
            "new_game": {
                "texture": arcade.load_texture(BTN_PATH + "start.png"),
                "pos": (col_gauche, ligne_haut),
                "action": self.start_game
            },
            "quizz": {
                "texture": arcade.load_texture(BTN_PATH + "quizz.png"),
                "pos": (col_droite, ligne_haut),
                "action": self.open_quizz
            },
            "settings": {
                "texture": arcade.load_texture(BTN_PATH + "settings.png"),
                "pos": (col_droite, ligne_milieu),
                "action": self.open_settings
            },
            "scoreboard": {
                "texture": arcade.load_texture(BTN_PATH + "score.png"),
                "pos": (col_gauche, ligne_milieu),
                "action": self.open_score
            },
            "exit": {
                "texture": arcade.load_texture(BTN_PATH + "end.png"),
                "pos": (col_centre, ligne_bas),
                "action": self.end_game
            }
        }

        # Menu music
        self.music = arcade.Sound("assets/music/mainMenu_theme.mp3")
        self.music.play(volume=1, loop=True)

    # +---------------------------------------------------------------------+
    # |                            Btn Methods                              |
    # +---------------------------------------------------------------------+

    def start_game(self):
        print("Lancement du jeu...")
        self.window.show_view(GameView())

    def open_quizz(self):
        print("Ouverture du quizz...")

    def open_settings(self):
        print("Ouverture des settings...")

    def open_score(self):
        print("Ouverture du scoreboards...")

    def end_game(self):
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
            x, y = data["pos"]
            arcade.draw_texture_rect(
                texture=data["texture"],
                rect=arcade.XYWH(x, y, self.btn_width, self.btn_height)
            )

    def on_mouse_press(self, x, y, button, modifiers):
        # La détection s'adapte aussi aux dimensions proportionnelles
        for nom, data in self.boutons.items():
            bx, by = data["pos"]
            
            if (bx - self.btn_width / 2 < x < bx + self.btn_width / 2 and 
                by - self.btn_height / 2 < y < by + self.btn_height / 2):
                
                data["action"]()
                break
