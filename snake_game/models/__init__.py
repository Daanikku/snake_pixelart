"""Modelos: lógica pura del juego (sin dependencias de pygame)."""
from snake_game.models.food import Food, Point
from snake_game.models.snake import Snake

__all__ = ["Snake", "Food", "Point"]