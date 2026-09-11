# Implementation Plan

**Objetivo:** Reorganizar el proyecto Snake en un paquete `snake_game/` con separación MVC estricta y mejorar la calidad del código (tipado, manejo de excepciones, rutas robustas, eliminación de código muerto), **sin cambiar ninguna funcionalidad ni añadir características**.

Se trata de un refactor 100 % conservador: mismo comportamiento, mismas probabilidades, mismos estados, misma persistencia. La lógica de juego actual (que ya sigue MVC dentro de `SnakeF.py`, 428 líneas) se extrae a módulos por responsabilidad. Se corrige a la vez calidad del código detectada en el análisis: constantes mágicas, `except:` desnudos, dependencia del directorio de trabajo (CWD), constante no usada (`EFFECT_DURATION`), asset cargado inexistente (`bg_input.png`) y `play_music()` llamado por frame.

Estructura elegida por el usuario: **paquete plano `snake_game/` en la raíz** + `main.py` como entry point.

---

## Types

Alias de tipos puros de Python (solo para legibilidad y verificación, no introducen dependencias):

```python
# snake_game/models/food.py
Point      = tuple[int, int]                      # (x, y) en la cuadrícula
FoodType   = Literal["normal", "bonus", "grow", "shrink", "speed_up", "slow"]

# snake_game/config.py
EffectName = Literal["Crecimiento", "Velocidad", "Lentitud"]
GameState  = Literal["menu", "game", "config", "death", "name_input"]

# snake_game/persistence/score_manager.py
ScoreEntry = TypedDict("ScoreEntry", {"name": str, "score": int})
```

Observaciones:
- Se declaran en el módulo donde se usan para evitar ciclos de import; `config` no necesita tipos.
- No se usan `@dataclass`/enums que cambien la semántica actual: las cadenas `"normal"`, `"menu"`, etc. se conservan literales idénticas para no alterar `ranking.json` ni las comparaciones.

---

## Files

### Archivos nuevos (ruta absoluta y propósito)

| Ruta | Propósito |
|---|---|
| `/home/daanik/Projects/Snake/main.py` | Entry point: importa `Game` y ejecuta `main()`. Sin otra lógica. |
| `/home/daanik/Projects/Snake/snake_game/__init__.py` | Exporta `Game` y `__version__ = "1.0.0"`. |
| `/home/daanik/Projects/Snake/snake_game/config.py` | Constantes extraídas de la sección 1 de `SnakeF.py` + constantes nuevas para números mágicos + rutas absolutas (`BASE_DIR`, `ASSETS_DIR`, `SCORE_FILE`, subcarpetas de assets). |
| `/home/daanik/Projects/Snake/snake_game/lcg.py` | Clase `LCG` (contenido de `LibreriaCongruencial.py`, sin cambios de algoritmo, con docstrings y type hints). |
| `/home/daanik/Projects/Snake/snake_game/rng.py` | Instancia global compartida `rng = LCG(seed=int(time.time()))` (equivalente exacto al `rng` global de `SnakeF.py`). |
| `/home/daanik/Projects/Snake/snake_game/models/__init__.py` | Exports de `Snake`, `Food`. |
| `/home/daanik/Projects/Snake/snake_game/models/snake.py` | Clase `Snake` (lógica pura, **sin imports de pygame**). |
| `/home/daanik/Projects/Snake/snake_game/models/food.py` | Clase `Food` + alias `Point`, `FoodType` (lógica pura, sin pygame). |
| `/home/daanik/Projects/Snake/snake_game/persistence/__init__.py` | Export de `ScoreManager`. |
| `/home/daanik/Projects/Snake/snake_game/persistence/score_manager.py` | Clase `ScoreManager` + tipo `ScoreEntry`. |
| `/home/daanik/Projects/Snake/snake_game/views/__init__.py` | Export de `View`. |
| `/home/daanik/Projects/Snake/snake_game/views/view.py` | Clase `View`: renderizado completo (fondos, serpiente, comida, HUD, menús). |
| `/home/daanik/Projects/Snake/snake_game/controllers/__init__.py` | Export de `Game`, `SoundManager`. |
| `/home/daanik/Projects/Snake/snake_game/controllers/audio.py` | Clase `SoundManager` (música y SFX). |
| `/home/daanik/Projects/Snake/snake_game/controllers/game.py` | Clase `Game` (orquestador, máquina de estados, entradas, bucle principal). |
| `/home/daanik/Projects/Snake/tests/__init__.py` | Paquete de tests. |
| `/home/daanik/Projects/Snake/tests/test_lcg.py` | Pruebas de `LCG` (reproducibilidad, rangos). |
| `/home/daanik/Projects/Snake/tests/test_snake.py` | Pruebas de `Snake` (movimiento, crecimiento, colisiones). |
| `/home/daanik/Projects/Snake/tests/test_food.py` | Pruebas de `Food` (posición válida, tipos, distribución con LCG seedeado). |
| `/home/daanik/Projects/Snake/tests/test_score_manager.py` | Pruebas de `ScoreManager` (top 5, round-trip con `tmp_path`). |
| `/home/daanik/Projects/Snake/tests/test_game_smoke.py` | Smoke test headless del juego completo (con `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy`). |
| `/home/daanik/Projects/Snake/implementation_plan.md` | Este documento. |

### Archivos que se ELIMINAN (después de migrar y validar)

| Ruta | Reemplazo |
|---|---|
| `/home/daanik/Projects/Snake/SnakeF.py` | Contenido repartido en `snake_game/` + `main.py`. |
| `/home/daanik/Projects/Snake/LibreriaCongruencial.py` | `snake_game/lcg.py`. |

> ⚠️ El directorio no es un repositorio git. Antes de borrar los originales se hace una copia de seguridad (`SnakeF.py`, `LibreriaCongruencial.py`, `ranking.json`) en `/tmp/snake_backup/` o carpeta elegida por el usuario.

### Archivos que NO cambian

- `/home/daanik/Projects/Snake/requirements.txt` → se mantiene `pygame==2.6.1`.
- `/home/daanik/Projects/Snake/assets/**` → se queda en la raíz; las rutas se resuelven desde `BASE_DIR` (independiente del CWD).
- `/home/daanik/Projects/Snake/ranking.json` → formato y ubicación (raíz) intactos.

---

## Functions

> Todas las funciones conservan los valores y el flujo exacto de `SnakeF.py`. Solo se añaden type hints, docstrings y mejoras de robustez (`except Exception` + `logger.warning(...)` en vez de `except:` desnudo).

### `snake_game/lcg.py`
- `LCG.__init__(self, seed: int, a: int = 1103515245, c: int = 12345, m: int = 32768) -> None` — sin cambios.
- `LCG.next_int(self) -> int` — sin cambios (mantener `self.Xn`/`self.a`/`self.c`/`self.m`).
- `LCG.random(self) -> float` — sin cambios.
- `LCG.randint(self, a: int, b: int) -> int` — sin cambios.
- `LCG.uniform(self, a: float, b: float) -> float` — sin cambios.
- `LCG.generate_list(self, n: int) -> list[float]` — sin cambios.

### `snake_game/rng.py`
- Variable de módulo: `rng: LCG = LCG(seed=int(time.time()))` — instancia global compartida (equivalente al `rng` de `SnakeF.py`).

### `snake_game/models/snake.py`
- `Snake.__init__(self) -> None` — misma posición inicial y `direction = (1, 0)`, `grow_pending = 0`.
- `Snake.set_direction(self, d: Point) -> None` — misma lógica anti-180°.
- `Snake.move(self) -> None` — misma lógica (insert cabeza, pop condicionado por `grow_pending`).
- `Snake.grow(self, n: int = 1) -> None` — igual.
- `Snake.shrink(self, n: int = 1) -> None` — usa `config.MIN_SNAKE_LENGTH` (era literal `3`).
- `Snake.collides(self) -> bool` — misma lógica con `GRID_W`/`GRID_H` de config.

### `snake_game/models/food.py`
- `Food.__init__(self, snake_body: list[Point], effect_active: bool, rng: LCG = RNG) -> None` — **nuevo parámetro `rng` con valor por defecto** (mantiene comportamiento; habilita tests deterministas).
- `Food.random_position(self, snake_body: list[Point]) -> Point` — mismo bucle; usa `self.rng`.
- `Food.random_type(self, effect_active: bool) -> FoodType` — **mismísima tabla de probabilidades** (50/15/15/10/7/3 sin efecto; 60/25/15 con efecto).

### `snake_game/persistence/score_manager.py`
- `ScoreManager.__init__(self, path: Path = SCORE_FILE) -> None` — **nuevo parámetro `path`** con valor por defecto = `config.SCORE_FILE` (habilita tests con archivo temporal).
- `ScoreManager.load(self) -> list[ScoreEntry]` — mismo comportamiento (archivo inexistente/corrupto → `[]`), `except Exception` + warning.
- `ScoreManager.save(self) -> None` — igual.
- `ScoreManager.add(self, name: str, score: int) -> None` — misma ordenación/re-corte a `config.TOP_SCORES` (era literal `5`).

### `snake_game/views/view.py`
- `View.__init__(self, screen: pygame.Surface) -> None` — carga fuente vía `_load_font()` (nuevo helper).
- `View._init_assets(self) -> None` — elimina la carga de `bg_input` (inexistente y sin uso); rutas desde `ASSETS_DIR` y subcarpetas.
- `View._load_img(self, path: Path, size: tuple[int, int]) -> pygame.Surface` — mismo fallback gris; `except Exception` + warning.
- `View._load_font(self) -> pygame.font.Font` — **nuevo**: intenta `pygame.font.Font(str(FONTS_DIR / "arcade.ttf"), 24)`; si falla, `pygame.font.SysFont("ArcadeClassic", 24)` (fallback que preserva el aspecto actual).
- `View.draw_game(...)` / `_render_text(...)` / `draw_menu(scores)` / `draw_config(sound_enabled)` / `draw_death()` / `draw_name_input(name, score)` — mismas firmas y posiciones de dibujo exactas.

### `snake_game/controllers/audio.py`
- `SoundManager.__init__(self) -> None` — `pygame.mixer.init()` ahora **protegido** con `try/except`; si no hay dispositivo de audio, `self.enabled = False` (antes podía crashear). Rutas desde config.
- `SoundManager.play_music(self, key: str) -> None` — misma guarda `current_music == key`.
- `SoundManager.play_sfx(self, key: str) -> None` — igual.
- `SoundManager.toggle(self) -> None` — igual.

### `snake_game/controllers/game.py`
- `Game.__init__(self) -> None` — mismo `pygame.init()`, pantalla 1280×720, caption `"Snake Evolution"`, composición de View/SoundManager/ScoreManager/Clock; añade `self._music_state: GameState | None = None`.
- `Game.reset(self) -> None` — idéntico; sustituye literales por constantes de config.
- `Game.handle_game_input(self) -> None` — idéntico (incluido `dir_lock`).
- `Game.handle_events(self) -> bool` — idéntico (menú 1/2/3, config S/ESC, death ENTER, name_input ENTER/BACKSPACE/alnum máx 10).
- `Game.update(self) -> None` — idéntico (expiración de efectos, movimiento temporalizado, colisión, comida).
- `Game._apply_food_logic(self) -> None` — idéntico en puntuación y efectos; constantes `FAST_DELAY`/`SLOW_DELAY`/`SPEED_EFFECT_DURATION`/`GROW_EFFECT_DURATION` (eran literales 60/200/5000/3000).
- `Game._set_effect(self, name: EffectName, duration: int) -> None` — igual.
- `Game._sync_music(self) -> None` — **nuevo helper interno**: `play_music("death" if self.state == "death" else "main")`, llamado solo cuando cambia `self.state` (reemplaza la llamada por frame de `run()`; resultado audible idéntico porque `play_music` ya se auto-guarda).
- `Game.run(self) -> None` — mismo bucle (events/update/draw según estado/flip/`clock.tick(FPS)`/`pygame.quit()`).

### `main.py`
- `main() -> None` → `Game().run()`.

---

## Classes

| Clase | Ruta | Cambio frente al original |
|---|---|---|
| `LCG` | `snake_game/lcg.py` | Trasladada de `LibreriaCongruencial.py`; solo docstrings + type hints. |
| `Snake` | `snake_game/models/snake.py` | Extraída de `SnakeF.py`; usa constantes de `config`. |
| `Food` | `snake_game/models/food.py` | Extraída; constructor acepta `rng` (default = instancia global). |
| `ScoreManager` | `snake_game/persistence/score_manager.py` | Extraída; constructor acepta `path` (default = config). |
| `View` | `snake_game/views/view.py` | Extraída; elimina `bg_input` muerto, usa fuentes y rutas por config. |
| `SoundManager` | `snake_game/controllers/audio.py` | Extraída; `mixer.init()` protegido, rutas por config. |
| `Game` | `snake_game/controllers/game.py` | Extraída; nuevo helper `_sync_music`, constantes de config. |

No se elimina ninguna clase ni se cambia herencia (todas son clases planas, sin herencia).

---

## Dependencies

- **Sin dependencias nuevas de runtime**: `pygame==2.6.1` se mantiene tal cual.
- **Tests**: solo `unittest` de la biblioteca estándar (cero dependencias de desarrollo nuevas).
- No se añaden `pytest`, `mypy` ni linters al `requirements.txt`.
- Importación interna: se usa `import snake_game.config as config` (o `from snake_game.config import ...`); `food.py` importa `from snake_game.rng import rng as RNG` y `from snake_game.lcg import LCG`.

### Grafo de dependencias (dirección única, sin ciclos)

```
main.py → controllers/game
controllers/game → config, models, persistence, views, controllers/audio
views → config
controllers/audio → config
persistence/score_manager → config
models/snake → config
models/food → rng, lcg, config
config → (nada)
```

---

## Testing

- **Nuevos tests (stdlib `unittest`, sin pygame)** en `tests/`:
  - `test_lcg.py`: misma seed → misma secuencia; `randint(a,b)` dentro de `[a,b]`; `random()` en `[0,1)`; `uniform` en `[a,b]`; `generate_list(n)` devuelve `n` valores.
  - `test_snake.py`: cuerpo inicial = 3 segmentos centrados; `move()` avanza en dirección; `grow(1)` impide pop en el siguiente movimiento; `shrink(n)` no baja de `MIN_SNAKE_LENGTH=3`; `set_direction` rechaza giro de 180°; `collides()` con borde (serpiente fuera de `GRID`) y auto-colisión.
  - `test_food.py`: con `LCG(seed=fijo)` → posición nunca dentro de `snake_body` y dentro del tablero; `random_type` devuelve solo valores válidos y respeta los umbrales de probabilidad sobre 10k muestras.
  - `test_score_manager.py`: `add` inserta/ordena/recorta a 5; round-trip carga/guarda con archivo temporal; archivo corrupto → `[]`.
  - `test_game_smoke.py`: con `SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy` (env vars ANTES de importar pygame), instancia `Game`, fuerza transiciones `menu → game → death → name_input → menu`, verifica que `score`, `snake` y `state` evolucionan sin excepción, y termina con `pygame.quit()`.

- **Validación (antes de borrar los archivos originales):**
  1. `python -m py_compile main.py snake_game/**/*.py` → sin errores.
  2. `python -m unittest discover -s tests -v` → todo verde.
  3. Smoke test headless: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m unittest tests.test_game_smoke -v`.
  4. Paridad de comportamiento: con la misma `seed` de `LCG`, `Food` y `Snake` producen los mismos resultados que los archivos originales (test comparativo en la fase de validación).
  5. Prueba manual del usuario: `python main.py` → misma experiencia, menú, ranking y sonidos.

---

## Implementation Order

1. **Backup**: copiar `SnakeF.py`, `LibreriaCongruencial.py` y `ranking.json` a una carpeta de respaldo externa (el directorio no es un repo git).
2. **Esqueleto del paquete**: crear `snake_game/` con `__init__.py` vacíos en `models/`, `persistence/`, `views/`, `controllers/`, y `snake_game/config.py` (constantes + rutas `BASE_DIR`/`ASSETS_DIR`/`SCORE_FILE`).
3. **LCG**: crear `snake_game/lcg.py` (traslado literal con type hints) y `snake_game/rng.py` (instancia global).
4. **Modelos**: `models/snake.py` y `models/food.py` (sin imports de pygame).
5. **Persistencia**: `persistence/score_manager.py`.
6. **Vista**: `views/view.py` (assets, fuentes, dibujado idéntico).
7. **Controladores**: `controllers/audio.py` y luego `controllers/game.py` (que depende de todos los anteriores).
8. **Entry point y API**: `main.py` y exports en `snake_game/__init__.py`.
9. **Tests**: crear `tests/` con los 5 ficheros de `unittest`.
10. **Validación**: compilar, ejecutar `unittest` completo y smoke test headless; corregir cualquier desvío de comportamiento.
11. **Limpieza**: eliminar `SnakeF.py` y `LibreriaCongruencial.py` (los originales quedan en el backup).
12. **Revisión final**: buscar números mágicos residuales y `except:` desnudos; confirmar que no quedan imports de `SnakeF`/`LibreriaCongruencial`; regenerar `__pycache__`.

---

## Nota de ejecución (2026-09-10)

- Se omitieron los tests de `tests/` por decisión del usuario ("procede pero sin crear tests").
- La validación se realizó con scripts temporales en `/tmp/` (no versionados):
  - `/tmp/snake_parity.py` → **PARITY OK**: LCG, `Food`, `Snake` y `ScoreManager` producen resultados idénticos a los módulos originales con las mismas seeds.
  - `/tmp/snake_smoke.py` → **SMOKE OK**: flujo completo headless `menu → game → death → name_input → menu`, toggle de sonido y salida por QUIT, tras borrar los originales.
  - `timeout 3 python main.py` → el juego arranca sin errores (termina por timeout, esperado en modo interactivo).
- Originales borrados tras validar; respaldo en `/tmp/snake_backup/` (`SnakeF.py`, `LibreriaCongruencial.py`, `ranking.json`).