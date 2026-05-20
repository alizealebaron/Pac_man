# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 16:14:42 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 16:12:29 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import argparse
import sys
from src.parsing.arg_parser import check_argument
from src.parsing.config_loader import ConfigLoader
from src.models.configmodel import ConfigModel
def main() -> None:
    try:
        arg: argparse.Namespace = check_argument()

        config: ConfigModel = ConfigLoader.load_config(arg.config_file)
        for e in config.model_fields:
            print(e)
        # print(f'highscore_filename: {config.highscore_filename} \n'
        #       f'level: {config.level}\n'
        #       f'lives: {config.lives}\n'
        #       f'pacgum: {config.pacgum}\n'
        #       f'points_per_pacgum: {config.points_per_pacgum}\n'
        #       f'points_per_super_pacgum: {config.points_per_super_pacgum}\n'
        #       f'points_per_ghost: {config.points_per_ghost}\n'
        #       f'seed: {config.seed}\n'
        #       f'level_max_time: {config.level_max_time}\n'
            # )
    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
