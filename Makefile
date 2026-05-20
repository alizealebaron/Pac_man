# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Makefile                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 16:14:58 by alebaron        #+#    #+#               #
#  Updated: 2026/05/20 09:46:09 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

MYPY_FLAGS	=  --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
UV_VERSION	= uv --version
UV_INSTALL	= curl -LsSf https://astral.sh/uv/install.sh | sh
SRC			= src pac-man.py
CONFIG		= 

install:
	@if ! $(UV_VERSION) > /dev/null 2>&1; then\
		$(UV_INSTALL); \
	fi
	@uv sync

run: install
	@uv run python -m pac-man $(CONFIG)

debug:
	@uv run python -m pdb -m pac-man $(CONFIG)

clean:
	@rm -rf .mypy_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	@rm -rf .venv

lint:
	@-uv run flake8 ${SRC}
	@-uv run mypy ${SRC} $(MYPY_FLAGS)

lint-strict:
	@-uv run flake8 ${SRC}
	@-uv run mypy ${SRC} $(MYPY_FLAGS) --strict

.PHONY: install run debug clean fclean lint lint-strict
.SILENT: