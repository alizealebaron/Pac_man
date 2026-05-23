# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  scoreboard_view.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/23 10:58:55 by alebaron        #+#    #+#               #
#  Updated: 2026/05/23 15:57:42 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/score_background.png"
MUSIC_PATH = "assets/music/scoreboard_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class ScoreboardView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        super().__init__(window)
        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.lst_score = self.window.manager.scoreboard

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
        """ Draw everything """
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

        # Affichage des scores
        self.draw_big_scoreboard()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_big_scoreboard(self):

        # Tri des 3 meilleurs
        scores = sorted(self.lst_score,
                        key=lambda p: p.score,
                        reverse=True)[:12]

        # Configuration des positions
        start_x = self.window.height / 2
        start_y = (self.window.width / 2) - 80
        line_height = 70
        icon_size = 50

        # Joueurs présents au top 3
        for i, player in enumerate(scores):

            current_y = start_y - (i * line_height)

            # Image de rang
            if (i < 12):
                rank_tex = arcade.load_texture(f"assets/rank/rank_{i+1}_64.png")
            else:
                rank_tex = arcade.load_texture("assets/rank/rank_0.png")
            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y,
                                 icon_size, icon_size)
            )

            # Image du pokémon
            pokemon = player.pokemon
            profile_tex = arcade.load_texture(f"assets/sprite/pokemon/{pokemon}/portraits/Normal.png") 
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 40, current_y,
                                 icon_size, icon_size)
            )

            sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
            arcade.draw_texture_rect(
                texture=sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 40, current_y,
                                 icon_size + 5, icon_size + 5)
            )

            # Nom + Score
            text_content = f"{player.name} ({player.score})"
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 30,
                                      current_y - 8,
                                      color=arcade.color.BLACK,
                                      font_size=16)
            player_name.draw()
