# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  save_score_view.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/28 14:12:22 by alebaron        #+#    #+#               #
#  Updated: 2026/05/29 14:42:08 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/save_score_background.png"
MUSIC_PATH = "assets/music/save_score_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class SaveScoreView(arcade.View):

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
            self.music = arcade.Sound(MUSIC_PATH)
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

        # Affichage du petit leaderboard
        self.draw_mid_leaderboard()

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_mid_leaderboard(self):

        leader_sprite = arcade.load_texture("assets/menu/"
                                            "small_leaderboard.png")
        w = self.window.width * 0.3
        h = self.window.height * 0.7
        arcade.draw_texture_rect(
            texture=leader_sprite,
            rect=arcade.XYWH(
                x=self.window.width / 2 + self.window.width / 2 * 0.5,
                y=self.window.height / 2,
                width=w,
                height=h
            )
        )

        # Tri des 3 meilleurs
        scores = sorted(self.window.manager.scoreboard,
                        key=lambda p: p.score,
                        reverse=True)[:9]

        # Configuration des positions
        start_x = self.window.height + 225
        start_y = (self.window.width / 2) - 175
        line_height = 70
        icon_size = 50

        # Joueurs présents au top 3
        for i, player in enumerate(scores):

            current_y = start_y - (i * line_height)

            # Image de rang
            if (i < 12):
                rank_tex = arcade.load_texture(f"assets/rank/rank_{i+1}_64."
                                               "png")
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
                                      font_size=12,
                                      font_name="FOT-Humming Pro")
            player_name.draw()

        i = len(scores)

        while (i < 3):

            current_y = start_y - (i * line_height)

            # Image de rang
            rank_tex = arcade.load_texture("assets/rank/rank_0.png")
            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y, icon_size, icon_size)
            )

            # Image du pokémon
            profile_tex = arcade.load_texture(f"assets/sprite/undefined/Normal.png") 
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y, icon_size, icon_size)
            )

            # Nom + Score
            text_content = "..."
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 20,
                                      current_y - 5,
                                      color=arcade.color.BLACK,
                                      font_size=11,
                                      font_name="FOT-Humming Pro")
            player_name.draw()

            i += 1

