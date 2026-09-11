"""Modelo de la serpiente.

Lógica pura (sin importar pygame): estructura, movimiento y colisiones.
"""
from snake_game import config
from snake_game.models.food import Point


class Snake:
    """Gestiona la estructura, movimiento y crecimiento de la serpiente."""

    def __init__(self) -> None:
        # Inicia en el centro con 3 segmentos
        self.body: list[Point] = [
            (config.GRID_W // 2, config.GRID_H // 2),
            (config.GRID_W // 2 - 1, config.GRID_H // 2),
            (config.GRID_W // 2 - 2, config.GRID_H // 2),
        ]
        self.direction: Point = (1, 0)
        self.grow_pending = 0

    def set_direction(self, d: Point) -> None:
        """Actualiza la dirección evitando giros de 180 grados."""
        if (d[0] * -1, d[1] * -1) != self.direction:
            self.direction = d

    def move(self) -> None:
        """Calcula la nueva posición de la cabeza y gestiona la cola."""
        x, y = self.body[0]
        new_head = (x + self.direction[0], y + self.direction[1])
        self.body.insert(0, new_head)

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, n: int = 1) -> None:
        """Incrementa el contador de crecimiento para el siguiente movimiento."""
        self.grow_pending += n

    def shrink(self, n: int = 1) -> None:
        """Reduce el tamaño de la serpiente sin bajar del mínimo."""
        removable = len(self.body) - config.MIN_SNAKE_LENGTH
        for _ in range(min(n, removable)):
            self.body.pop()

    def collides(self) -> bool:
        """Verifica colisiones con bordes o con el propio cuerpo."""
        x, y = self.body[0]
        out_of_bounds = x < 0 or x >= config.GRID_W or y < 0 or y >= config.GRID_H
        self_collision = self.body[0] in self.body[1:]
        return out_of_bounds or self_collision