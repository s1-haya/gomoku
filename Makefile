
NAME := Gomoku
PYTHON := python

.PHONY: all clean fclean re install test venv

all:

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests -v

clean:

fclean: clean

re: fclean all
