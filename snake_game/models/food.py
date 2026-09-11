"""Modelo de la comida.

Lógica pura (sin importar pygame): aparición y tipo de los ítems consumibles.
El parámetro `rng` se inyecta para permitir pruebas deterministas; por
defecto usa la instancia global compartida (equivalente al `rng` de
`SnakeF.py`).
"""
from typing import Literal

from snake_game import config
from snake_game.lcg import LCG
from snake_game.rng import rng as RNG

Point = tuple[int, int]
FoodType = Literal["normal", "bonus", "grow", "shrink", "speed_up", "slow"]


class Food:
    """Gestiona la aparición y el tipo de ítems consumibles."""

    def __init__(self, snake_body: list[Point], effect_active: bool, rng: LCG = RNG) -> None:
        self.rng = rng
        self.type = self.random_type(effect_active)
        self.pos = self.random_position(snake_body)

    def random_position(self, snake_body: list[Point]) -> Point:
        """Genera una posición aleatoria que no esté ocupada por la serpiente."""
        while True:
            p = (self.rng.randint(0, config.GRID_W - 1), self.rng.randint(0, config.GRID_H - 1))
            if p not in snake_body:
                return p

    def random_type(self, effect_active: bool) -> FoodType:
        """Determina el tipo de comida según probabilidades (idéntico al original)."""
        r = self.rng.random()
        # Si ya hay un efecto, reducimos la aparición de power-ups de estado
        if effect_active:
            if r < 0.6:
                return "normal"
            if r < 0.85:
                return "bonus"
            return "shrink"

        # Probabilidades estándar
        if r < 0.50:
            return "normal"
        if r < 0.65:
            return "speed_up"
        if r < 0.80:
            return "slow"
        if r < 0.90:
            return "grow"
        if r < 0.97:
            return "shrink"
        return "bonus"