# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  configmodel.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 11:08:47 by rruiz           #+#    #+#               #
#  Updated: 2026/05/19 14:25:03 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field
from typing import Optional

class LevelConfig(BaseModel):
    name: str = Field(min_length=1, default='map')
    width: int = Field(ge=1, le=500, default=10)
    height: int = Field(ge=1, le=500, default=10)


class ConfigModel(BaseModel):
    highscore_filename: Optional[str] = Field(default="highscores.json", min_length=1)
    level: list[LevelConfig] = Field(min_length=1)
    lives: int = Field(ge=1, le=1000, default=3)
    pacgum: int = Field(ge=1, le=1000, default=42)
    points_per_pacgum: int = Field(ge=1, le=1000, default=10)
    points_per_super_pacgum: int = Field(ge=1, le=1000, default=50)
    points_per_ghost: int = Field(ge=1, le=1000, default=100)
    seed: int = Field(ge=0, default=42)
    level_max_time: int = Field(ge=1, le=3600, default=90)
