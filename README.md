# 🐍 Snake Evolution

Juego clásico de **Snake** desarrollado en **Python** con **Pygame**. Proyecto académico cuya característica distintiva es el uso de un **generador de números aleatorios por congruencia lineal (LCG)** implementado desde cero, en lugar del módulo `random` de Python.

## ✨ Características

- 🕹️ Mecánica clásica de Snake (movimiento por celdas, crecimiento, colisiones).
- 🍎 **6 tipos de comida** con efectos distintos: `normal`, `bonus`, `speed_up`, `slow`, `grow` y `shrink`.
- ⚡ Power-ups con duración limitada (velocidad, lentitud, crecimiento).
- 🏆 **Top 5 de puntuaciones** persistido en `ranking.json` (nombre + puntuación).
- 🎵 Música de fondo y efectos de sonido.
- 🎨 Sprites y fondos propios; fallbacks automáticos si falta algún asset.
- 🔢 Generador aleatorio **LCG** propio (`a=1103515245, c=12345, m=32768`), con período completo de 32768.

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC (Modelo-Vista-Controlador)** con una separación estricta de responsabilidades:

```
Snake/
├── main.py                      # Punto de entrada
├── snake_game/
│   ├── config.py                # Constantes y rutas del juego
│   ├── lcg.py                   # Generador LCG (implementación propia)
│   ├── rng.py                   # Instancia global del generador
│   ├── models/                  # LOGICA (sin dependencias de pygame)
│   │   ├── snake.py             #   Serpiente: movimiento, crecimiento, colisiones
│   │   └── food.py              #   Comida: tipos y posiciones aleatorias
│   ├── persistence/             # DATOS
│   │   └── score_manager.py     #   Ranking top 5 (JSON)
│   ├── views/                   # VISTA
│   │   └── view.py              #   Renderizado de la partida y menús
│   └── controllers/             # CONTROLADORES
│       ├── game.py              #   Orquestador y máquina de estados
│       └── audio.py             #   Música y efectos de sonido
├── assets/                      # Sprites, fondos, sonidos y fuentes
└── ranking.json                 # Puntuaciones guardadas
```

Flujo principal: `main.py → Game.run()` → bucle `handle_events / update / draw` → `pygame.display.flip()`.

## 🚀 Instalación y ejecución

Requisitos: **Python 3.10+**.

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd Snake

# 2. Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Jugar
python main.py
```

> **Controles:** menú `1` jugar / `2` opciones / `3` salir · flechas para mover la serpiente · `S` activar/desactivar sonido · `ESC` volver · `Enter` confirmar.

> 💡 El juego incluye fallbacks: si falta un asset o no hay dispositivo de audio, continúa sin imágenes/sonido en lugar de fallar.

## 🧪 Pruebas

El comportamiento se validó mediante pruebas de paridad y smoke tests (headless con `SDL_VIDEODRIVER=dummy`).

## 📚 Contexto académico

La clase `LCG` en `snake_game/lcg.py` implementa la recurrencia:

```
Xn+1 = (a·Xn + c) mod m      con a=1103515245, c=12345, m=32768
```

Este generador sustituye al módulo `random` de Python como ejercicio de implementación de generadores pseudoaleatorios.