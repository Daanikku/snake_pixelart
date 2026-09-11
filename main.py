"""Punto de entrada del juego Snake Evolution."""
from snake_game.controllers.game import Game


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()