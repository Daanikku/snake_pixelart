"""Controlador principal: orquestación, entrada y máquina de estados."""
import pygame

from snake_game import config
from snake_game.controllers.audio import SoundManager
from snake_game.models.food import Food
from snake_game.models.snake import Snake
from snake_game.persistence.score_manager import ScoreManager
from snake_game.rng import rng
from snake_game.views.view import View


class Game:
    """Orquestador principal del juego."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Snake Evolution")

        self.view = View(self.screen)
        self.sound = SoundManager()
        self.scores = ScoreManager()
        self.clock = pygame.time.Clock()

        self.state: config.GameState = "menu"
        self.name_input = ""
        self.reset()

        # Evita múltiples giros por paso
        self.dir_lock = False
        # Sync de música: solo cuando cambian estado o ajuste de sonido
        self._music_state: config.GameState | None = None
        self._music_dirty = False

    def reset(self) -> None:
        """Reinicia las variables para una nueva partida."""
        self.snake = Snake()
        self.food = Food(self.snake.body, False)
        self.score = 0
        self.move_delay = config.MOVE_DELAY
        self.last_move = 0
        self.effect = None
        self.effect_end = 0

    def handle_game_input(self) -> None:
        if self.dir_lock:
            return  # Si ya giramos en este paso, ignorar otras teclas

        keys = pygame.key.get_pressed()
        new_dir = None

        if keys[pygame.K_UP]:
            new_dir = (0, -1)
        elif keys[pygame.K_DOWN]:
            new_dir = (0, 1)
        elif keys[pygame.K_LEFT]:
            new_dir = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            new_dir = (1, 0)

        if new_dir:
            # Intentamos cambiar la dirección
            old_dir = self.snake.direction
            self.snake.set_direction(new_dir)
            # Si la dirección realmente cambió, bloqueamos hasta el próximo movimiento
            if self.snake.direction != old_dir:
                self.dir_lock = True

    def handle_events(self) -> bool:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if e.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if e.key == pygame.K_1:
                        self.state = "game"
                    elif e.key == pygame.K_2:
                        self.state = "config"
                    elif e.key == pygame.K_3:
                        return False

                elif self.state == "config":
                    if e.key == pygame.K_s:
                        self.sound.toggle()
                        self._music_dirty = True
                    elif e.key == pygame.K_ESCAPE:
                        self.state = "menu"

                elif self.state == "death":
                    if e.key == pygame.K_RETURN:
                        self.state = "name_input"
                        self.name_input = ""

                elif self.state == "name_input":
                    if e.key == pygame.K_RETURN and self.name_input:
                        self.scores.add(self.name_input, self.score)
                        self.reset()
                        self.state = "menu"
                    elif e.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif len(self.name_input) < config.MAX_NAME_LEN and e.unicode.isalnum():
                        self.name_input += e.unicode
        return True

    def update(self) -> None:
        """Actualiza la lógica del juego."""
        if self.state != "game":
            return

        # Control de Dirección
        self.handle_game_input()

        # Expiración de Efectos
        now = pygame.time.get_ticks()
        if self.effect and now > self.effect_end:
            self.effect = None
            self.move_delay = config.MOVE_DELAY

        # Movimiento temporalizado
        if now - self.last_move > self.move_delay:
            self.snake.move()
            self.last_move = now
            self.dir_lock = False  # Reiniciar bloqueo de dirección después de mover

            if self.snake.collides():
                self.state = "death"
                return

            if self.snake.body[0] == self.food.pos:
                self.sound.play_sfx("eat")
                self._apply_food_logic()
                self.food = Food(self.snake.body, self.effect is not None)

    def _apply_food_logic(self) -> None:
        """Procesa las consecuencias de comer."""
        t = self.food.type
        if t not in ["shrink", "grow"]:
            self.snake.grow(1)

        if t == "normal":
            self.score += 1
        elif t == "bonus":
            self.score += 3
        elif t == "shrink":
            self.snake.shrink(rng.randint(1, 2))
            self.score = max(0, self.score - 1)
        elif t == "grow":
            self.snake.grow(rng.randint(2, 4))
            self._set_effect("Crecimiento", config.GROW_EFFECT_DURATION)
        elif t == "speed_up":
            self.move_delay = config.FAST_DELAY
            self._set_effect("Velocidad", config.SPEED_EFFECT_DURATION)
        elif t == "slow":
            self.move_delay = config.SLOW_DELAY
            self._set_effect("Lentitud", config.SPEED_EFFECT_DURATION)

    def _set_effect(self, name: config.EffectName, duration: int) -> None:
        self.effect = name
        self.effect_end = pygame.time.get_ticks() + duration

    def _sync_music(self) -> None:
        """Reproduce la música correspondiente al estado actual."""
        key = "death" if self.state == "death" else "main"
        self.sound.play_music(key)

    def run(self) -> None:
        """Bucle principal."""
        running = True
        while running:
            running = self.handle_events()
            self.update()

            # Gestión de Audio: solo ante cambios de estado o del ajuste
            if self._music_state != self.state or self._music_dirty:
                self._sync_music()
                self._music_state = self.state
                self._music_dirty = False

            # Dibujado según estado
            if self.state == "game":
                remaining = max(0, self.effect_end - pygame.time.get_ticks())
                self.view.draw_game(self.snake, self.food, self.score, self.effect, remaining)
            elif self.state == "menu":
                self.view.draw_menu(self.scores.scores)
            elif self.state == "config":
                self.view.draw_config(self.sound.enabled)
            elif self.state == "death":
                self.view.draw_death()
            elif self.state == "name_input":
                self.view.draw_name_input(self.name_input, self.score)

            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()