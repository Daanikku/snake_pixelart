"""Persistencia del ranking de puntuaciones.

El parámetro `path` se inyecta para permitir pruebas con archivos
temporales; por defecto usa `config.SCORE_FILE` (comportamiento original).
"""
import json
import logging
from pathlib import Path
from typing import TypedDict

from snake_game import config

logger = logging.getLogger(__name__)

ScoreEntry = TypedDict("ScoreEntry", {"name": str, "score": int})


class ScoreManager:
    """Maneja la carga y guardado del Top 5 de puntuaciones."""

    def __init__(self, path: Path = config.SCORE_FILE) -> None:
        self.path: Path = path
        self.scores: list[ScoreEntry] = self.load()

    def load(self) -> list[ScoreEntry]:
        if not self.path.exists():
            return []
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("No se pudo cargar el ranking %s: %s", self.path, e)
            return []

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.scores, f)

    def add(self, name: str, score: int) -> None:
        """Añade puntuación, ordena y mantiene solo los mejores."""
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[: config.TOP_SCORES]
        self.save()