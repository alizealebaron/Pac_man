# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 16:14:42 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 09:35:54 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import argparse
import sys
from src.parsing.arg_parser import check_argument
from src.parsing.config_loader import ConfigLoader

def main() -> None:
    try:
        arg: argparse.Namespace = check_argument()

        config = ConfigLoader.load_config(arg.config_file)
    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
