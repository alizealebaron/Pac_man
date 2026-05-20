# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  arg_parser.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 09:22:52 by rruiz           #+#    #+#               #
#  Updated: 2026/05/20 16:50:06 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import argparse


def check_argument() -> argparse.Namespace:
    parse = argparse.ArgumentParser()
    parse.add_argument(
        'config_file',
        type=str,
        help='Path to the configuration file',
        nargs='?',
        default=None
    )
    arg: argparse.Namespace = parse.parse_args()

    return arg
