# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_loader.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 10:07:49 by rruiz           #+#    #+#               #
#  Updated: 2026/05/20 09:34:51 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
from typing import Any
import sys
from pydantic import ValidationError
from src.models.configmodel import ConfigModel

class ConfigLoader:
    default_config = {
        'highscore_filename': 'highscores.json',
        'level': [
            {'name': 'map1', 'width': 10, 'height': 10},
            {'name': 'map2', 'width': 11, 'height': 11},
            {'name': 'map3', 'width': 12, 'height': 12},
            {'name': 'map4', 'width': 13, 'height': 13},
            {'name': 'map5', 'width': 14, 'height': 14},
            {'name': 'map6', 'width': 15, 'height': 15},
            {'name': 'map7', 'width': 16, 'height': 16},
            {'name': 'map8', 'width': 17, 'height': 17},
            {'name': 'map9', 'width': 18, 'height': 18},
            {'name': 'map10', 'width': 19, 'height': 19}
        ],
        'lives': 3,
        'pacgum': 42,
        'points_per_pacgum': 10,
        'points_per_super_pacgum': 50,
        'points_per_ghost': 200,
        'seed': 42,
        'level_max_time': 90
        }


    @staticmethod
    def load_config(config_file_path: str | None) -> ConfigModel:
        config: dict[str, Any] = {}
 
        if config_file_path:
            config = ConfigLoader._clean_config(config_file_path)

        if not config:
            config = ConfigLoader.default_config

        try:
            return ConfigModel(**config)
        except ValidationError as e:
            print(f'Warning: config validation error: {e}'
                  '; using default configuration', file=sys.stderr)
            return ConfigModel(**ConfigLoader.default_config)



    @staticmethod
    def _clean_config(config_file_path: str) -> dict[str, Any]:
        try:
            with open(config_file_path, 'r') as f:
                config = f.read()
        except OSError as e:
            print(f'Warning: cannot open \'{config_file_path}\': {e}'
                  '; using default configuration', file=sys.stderr)
            return {}

        clean_lines = []
        for line in config.splitlines():
            no_comment = line.split('#')[0]
            clean_lines.append(no_comment)

        clean_config = '\n'.join(clean_lines)

        try:
            data: dict[str, Any] = json.loads(clean_config)
        except json.JSONDecodeError as e:
            print(f'Warning: invalid JSON in \'{config_file_path}\': {e}'
                  '; using default configuration', file=sys.stderr)
            return {}

        return data
