# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  personnality_view.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/26 01:33:59 by alebaron        #+#    #+#               #
#  Updated: 2026/05/26 04:13:42 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/personnality_background.png"
MUSIC_PATH = "assets/music/personnality_theme.mp3"

SELECTED_PATH = "assets/quizz/question_selected.png"
UNSELECTED_PATH = "assets/quizz/question_unselected.png"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PersonnalityView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window

        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation de la musique
        self.music_player = None

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=1, loop=True)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Affichage du background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

        # Affichage du bouton retour
        retour_sprite = arcade.load_texture("assets/button/retour.png")
        height = 90
        width = 170
        arcade.draw_texture_rect(
            texture=retour_sprite,
            rect=arcade.XYWH(45,
                             (self.window.height) - (height / 2),
                             width,
                             height)
        )

        # Affichage du premier message
        self.draw_begin_text()

        # Affichage des deux premières réponses
        reponses = ["Oui", "Non"]
        selected_reponse = reponses[0]

        start_y = self.window.height * 0.75
        space_between = 150

        for reponse in reponses:

            if (reponse is selected_reponse):
                question_sprite = arcade.load_texture(SELECTED_PATH)
            else:
                question_sprite = arcade.load_texture(UNSELECTED_PATH)

            arcade.draw_texture_rect(
                texture=question_sprite,
                rect=arcade.XYWH(150, start_y,
                                 self.window.width * 0.8,
                                 self.window.height * 0.2)
            )

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                            Draw methods                             |
    # +---------------------------------------------------------------------+

    def draw_begin_text(self):
        
        text_content = "Vous vous apprêtez à réaliser un test de personnalité"
        text_content += " pour déterminer votre Pokémon."
        texte = arcade.Text(text_content,
                            420,
                            200,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro")
        texte.draw()

        text_content = "Cela prendra quelques minutes."
        texte = arcade.Text(text_content,
                            750,
                            150,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro")
        texte.draw()

        text_content = "Voulez-vous continuer ?"
        texte = arcade.Text(text_content,
                            810,
                            95,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro")
        texte.draw()