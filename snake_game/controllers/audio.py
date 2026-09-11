"""Controlador de audio: música de fondo y efectos de sonido."""
import logging

import pygame

from snake_game import config

logger = logging.getLogger(__name__)


class SoundManager:
    """Controla la música y efectos de sonido."""

    def __init__(self) -> None:
        # Si no hay dispositivo de audio, el juego continúa sin sonido
        try:
            pygame.mixer.init()
            self.enabled = True
        except Exception as e:
            logger.warning("No hay dispositivo de audio (%s); sonido desactivado.", e)
            self.enabled = False
        self.current_music: str | None = None
        # Definición de rutas (pueden fallar si no existen archivos)
        self.music_files = {
            "main": str(config.SOUND_DIR / "main.mp3"),
            "death": str(config.SOUND_DIR / "death.mp3"),
        }
        try:
            self.sfx_eat = pygame.mixer.Sound(str(config.SOUND_DIR / "eat.wav"))
        except Exception as e:
            logger.warning("SFX eat no disponible (%s).", e)
            self.sfx_eat = None

    def play_music(self, key: str) -> None:
        if not self.enabled or self.current_music == key:
            return
        try:
            pygame.mixer.music.load(self.music_files[key])
            pygame.mixer.music.play(-1)
            self.current_music = key
        except Exception as e:
            logger.warning("No se pudo reproducir música %s: %s", key, e)

    def play_sfx(self, key: str) -> None:
        if self.enabled and key == "eat" and self.sfx_eat:
            self.sfx_eat.play()

    def toggle(self) -> None:
        self.enabled = not self.enabled
        if not self.enabled:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                logger.warning("No se pudo detener la música (%s).", e)
        else:
            self.current_music = None  # Reiniciar