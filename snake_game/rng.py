"""Instancia global del generador aleatorio.

Equivalente exacto al `rng = LCG(seed=int(time.time()))` de `SnakeF.py`.
"""
import time

from snake_game.lcg import LCG

rng = LCG(seed=int(time.time()))