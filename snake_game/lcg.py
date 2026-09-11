"""Generador de números aleatorios por congruencia lineal (LCG).

Clase trasladada de `LibreriaCongruencial.py` **sin cambios de algoritmo**.
Se usa en lugar del módulo `random` de Python como recurso educativo.
"""


class LCG:
    """Generador congruencial lineal: Xn+1 = (a * Xn + c) mod m."""

    def __init__(self, seed: int, a: int = 1103515245, c: int = 12345, m: int = 32768) -> None:
        self.Xn = seed
        self.a = a
        self.c = c
        self.m = m

    def next_int(self) -> int:
        # Xn+1 = (aXn + c) % m
        self.Xn = (self.a * self.Xn + self.c) % self.m
        return self.Xn

    def random(self) -> float:
        # número entre 0 y 1
        return self.next_int() / self.m

    def randint(self, a: int, b: int) -> int:
        return a + int(self.random() * (b - a + 1))

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.random()

    def generate_list(self, n: int) -> list[float]:
        return [self.random() for _ in range(n)]