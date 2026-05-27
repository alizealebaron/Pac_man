# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  quizz_view.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/26 04:44:09 by alebaron        #+#    #+#               #
#  Updated: 2026/05/27 16:07:39 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import time
import arcade
import random
from typing import Any, List
from src.models.questionModel import QuestionModel

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

class QuizzView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window, music_player: Any, music: Any):
        super().__init__()

        self.window = window

        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation de la musique
        self.music_player = music_player
        self.music = music

        # Initalisation des questions
        self.lst_questions = self.random_question()
        self.index_question = 0

        # Initialisation des réponses
        self.reponses = []
        self.selected_reponse = 0

        # Initialisation du caractère
        self.dict_caracteres = self.get_dict_caracteres()
        self.caractere = None
        self.index_carac = 0

        # Pokémon généré
        self.random_pokemon = None

    # +---------------------------------------------------------------------+
    # |                            Init Methods                             |
    # +---------------------------------------------------------------------+

    def get_dict_caracteres(self):

        dict_carac = {}
        lst_carac = self.window.manager.data_questions.caracteres

        for carac in lst_carac:
            dict_carac[carac] = 0

        return dict_carac

    def random_question(self) -> List[QuestionModel]:

        random.seed(int(time.time()))

        lst_questions = self.window.manager.data_questions.questions
        lst_questions: List[QuestionModel] = list(lst_questions.values())

        temp_question = lst_questions.pop(len(lst_questions) - 1)
        lst_questions = random.sample(lst_questions, 10)
        lst_questions.append(temp_question)

        return lst_questions

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

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

        # Affichage de la question actuelle
        if self.index_question < len(self.lst_questions):
            self.draw_actual_question()
        elif (self.index_question == len(self.lst_questions) and
              self.index_carac != -2):
            self.write_end_text()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.Z:
            self.selected_reponse = ((self.selected_reponse + 1) %
                                     len(self.reponses))

        if key == arcade.key.S:
            self.selected_reponse = ((self.selected_reponse - 1) %
                                     len(self.reponses))

        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.selected_reponse = 0
            if self.index_question < len(self.lst_questions):
                self.update_score()
                self.index_question += 1
            elif self.index_carac == -2:
                self.window.manager.player.pokemon = self.random_pokemon.name
                self.music.stop(self.music_player)
                self.window.show_view(self.window.start_view)
            elif self.index_question == len(self.lst_questions):
                self.index_carac += 1

    # +---------------------------------------------------------------------+
    # |                           Update Methods                            |
    # +---------------------------------------------------------------------+

    def update_score(self):

        reponse = self.reponses[self.selected_reponse]

        for score in reponse.scores:
            self.dict_caracteres[score] += reponse.scores[score]

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_pokemon(self):

        possible_pokemon = [obj for obj in self.window.manager.pokemons
                            if obj.comportement == self.caractere]

        if self.random_pokemon is None:
            self.random_pokemon = random.choice(possible_pokemon)

        sprite = arcade.load_texture(f"assets/sprite/pokemon/"
                                     f"{self.random_pokemon.name}"
                                     "/portraits/Normal.png")
        sprite_size = 150

        arcade.draw_texture_rect(
            texture=sprite,
            rect=arcade.XYWH(self.width / 2,
                             self.height / 2,
                             sprite_size,
                             sprite_size)
        )

        sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        arcade.draw_texture_rect(
            texture=sprite_frame,
            rect=arcade.XYWH(self.width / 2,
                             self.height / 2,
                             sprite_size + 15,
                             sprite_size + 15)
        )

        center_x = self.width / 2
        center_y = self.height / 2
        texte = arcade.Text(self.random_pokemon.name,
                            center_x,
                            center_y - sprite_size / 2 - 40,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")

        texte.draw()

    def write_end_text(self):

        self.caractere = max(self.dict_caracteres,
                             key=lambda key: self.dict_caracteres[key])

        if (self.index_carac > 0):

            data_questions = self.window.manager.data_questions
            lst_phrase = data_questions.caracteres[self.caractere].split("\n")

            center_x = self.width / 2
            center_y = self.height / 2
            texte = arcade.Text(lst_phrase[self.index_carac],
                                center_x,
                                center_y,
                                align="center",
                                color=arcade.color.WHITE,
                                font_size=20,
                                font_name="FOT-Humming Pro",
                                anchor_x="center",
                                anchor_y="center")

            texte.draw()

            if ((len(lst_phrase) - 1) == self.index_carac):
                self.index_carac = -1
        else:
            self.draw_pokemon()
            self.index_carac = -2

    def draw_actual_question(self):

        # Récupération des données
        act_q = self.lst_questions[self.index_question]
        self.reponses = act_q.reponses
        nb_reponses = len(self.reponses)

        # Initialisation des positions initiales
        center_height = self.height * 0.7
        space_between = 150

        sprite_width = self.window.width * 0.5
        sprite_height = self.window.height * 0.09

        # Formule pour la hauteur totale du bloc de réponses
        total_height = ((nb_reponses * sprite_height) +
                        ((nb_reponses - 1) * space_between))

        # Calcul du premier start_y (le sprite du bas)
        start_y = center_height - (total_height / 2) + (sprite_height / 2)

        for reponse in self.reponses:

            if (reponse is self.reponses[self.selected_reponse]):
                question_sprite = arcade.load_texture(SELECTED_PATH)
            else:
                question_sprite = arcade.load_texture(UNSELECTED_PATH)

            center_x = self.width / 2
            center_y = start_y

            arcade.draw_texture_rect(
                texture=question_sprite,
                rect=arcade.XYWH(center_x, center_y, sprite_width,
                                 sprite_height)
            )

            texte = arcade.Text(
                text=reponse.reponse,
                x=center_x,
                y=center_y,
                color=arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )
            texte.draw()

            start_y += space_between

        center_x = self.width / 2
        center_y = 200
        texte = arcade.Text(act_q.texte,
                            center_x,
                            center_y,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")
        texte.draw()
