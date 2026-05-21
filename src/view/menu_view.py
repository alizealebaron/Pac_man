# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 10:28:01 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 21:55:11 by alebaron        ###   ########.fr        #
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
        self.largeur = self.window.width
        self.hauteur = self.window.height

        # Calcul des dimensions proportionnelles des boutons
        self.btn_width = self.largeur * 0.20
        self.btn_height = self.hauteur * 0.17

        # Calcul des positions (en % de l'écran)
        col_gauche = self.largeur * 0.35
        col_droite = self.largeur * 0.65
        col_centre = self.largeur * 0.50

        ligne_haut = self.hauteur * 0.75
        ligne_milieu = self.hauteur * 0.48
        ligne_bas = self.hauteur * 0.20

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

        # Affichage du fond d'écran
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

        # Affichage des boutons du menu
        for nom, data in self.boutons.items():
            x, y = data["pos"]
            arcade.draw_texture_rect(
                texture=data["texture"],
                rect=arcade.XYWH(x, y, self.btn_width, self.btn_height)
            )

        # Affichage du joueur et de son nom

        sprite = arcade.load_texture("assets/sprite/test_face.png")
        sprite_size = 75

        arcade.draw_texture_rect(
            texture=sprite,
            rect=arcade.XYWH((sprite_size / 2) + 10,
                             (self.hauteur - (sprite_size / 2) - 10),
                             sprite_size,
                             sprite_size)
        )

        sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        arcade.draw_texture_rect(
            texture=sprite_frame,
            rect=arcade.XYWH((sprite_size / 2) + 10,
                             (self.hauteur - (sprite_size / 2) - 10),
                             sprite_size + 9,
                             sprite_size + 9)
        )

        player_name = arcade.Text("Anonyme_544895",
                                  sprite_size + 25,
                                  (self.hauteur - (sprite_size / 2) - 20),
                                  color=arcade.color.BLACK,
                                  font_size=20,
                                  font_name="Comic Sans MS")
        player_name.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # La détection s'adapte aussi aux dimensions proportionnelles
        for nom, data in self.boutons.items():
            bx, by = data["pos"]
            
            if (bx - self.btn_width / 2 < x < bx + self.btn_width / 2 and 
                by - self.btn_height / 2 < y < by + self.btn_height / 2):
                
                data["action"]()
                break
