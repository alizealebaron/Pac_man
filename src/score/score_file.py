# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  score_file.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 10:50:34 by alebaron        #+#    #+#               #
#  Updated: 2026/05/21 11:46:53 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import json
from src.models.scoreModel import Score


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

def retrieve_score_from_json(file: str):

    lst_score = []

    try:
        with open(file, "r") as file:
            data = json.load(file)
            lst_score = [Score(**arg) for arg in data]
    except json.JSONDecodeError as e:
        raise (e)
    except Exception:
        pass

    return lst_score
