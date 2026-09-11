# 🐍 Snake Evolution

Juego clásico de **Snake** desarrollado en **Python** con **Pygame**. Proyecto académico cuya característica distintiva es el uso de un **generador de números aleatorios por congruencia lineal (LCG)** implementado desde cero, en lugar del módulo `random` de Python.

## ✨ Características

- 🕹️ Mecánica clásica de Snake (movimiento por celdas, crecimiento, colisiones).
- 🍎 **6 tipos de comida** con efectos distintos: `normal`, `bonus`, `speed_up`, `slow`, `grow` y `shrink`.
- ⚡ Power-ups con duración limitada (velocidad, lentitud, crecimiento).
- 🏆 **Top 5 de puntuaciones** persistido en `ranking.json` (nombre + puntuación).
- 🎵 Música de fondo y efectos de sonido.
- 🎨 Sprites propios; fondos generados por IA y un sonido con referencia externa (ver [Atribución de assets](#-atribución-de-assets)); fallbacks automáticos si falta algún asset.
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
git clone https://github.com/Daanikku/snake_pixelart.git
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

## 🙏 Atribución de assets

Este proyecto incluye recursos generados con **inteligencia artificial** y una **referencia sonora** a un videojuego comercial. A continuación se detalla el origen de cada asset para dar el crédito correspondiente y evitar malentendidos.

### 🖼️ Fondos generados por IA

| Asset | Origen |
|-------|--------|
| `assets/background/bg_menu.png` | Generado con **ChatGPT (OpenAI)** |
| `assets/background/bg_death.png` | Generado con **ChatGPT (OpenAI)** |
| `assets/background/bg_name_input.png` | Generado con **ChatGPT (OpenAI)** |
| `assets/background/bg_config.png` | Generado con **IA** |

### 🔊 Efectos de sonido

| Asset | Origen |
|-------|--------|
| `assets/sound/death.mp3` | **Referencia** al sonido de muerte del videojuego **Dark Souls** (© **FromSoftware** / **Bandai Namco Entertainment**) |

> ℹ️ `death.mp3` es una **referencia/homenaje** al sonido característico de *Dark Souls*: no es un asset original del proyecto. Los derechos del sonido original pertenecen a sus autores.

### ✍️ Resto de assets

Los sprites de la serpiente (`assets/snake/`) y de la comida (`assets/food/`), la fuente `arcade.ttf` y los sonidos `eat.wav` y `main.mp3` son de **elaboración propia** del autor.

## ⚖️ Aviso legal

- Este proyecto tiene un **propósito exclusivamente académico y sin ánimo de lucro** (portfolio/currículum).
- El sonido `death.mp3` es un **homenaje/referencia** al sonido de muerte de *Dark Souls* de **FromSoftware** (publicado por **Bandai Namco Entertainment**). No se pretende infringir los derechos de autor ni de marca de sus titulares.
- Los fondos generados por IA se utilizan conforme a los **términos de uso** de la herramienta empleada (ChatGPT / OpenAI).
- Para un uso **comercial o público**, se recomienda sustituir `death.mp3` y los fondos generados por IA por recursos con licencia libre (CC0, CC-BY, etc.).

## 📚 Contexto académico

La clase `LCG` en `snake_game/lcg.py` implementa la recurrencia:

```
Xn+1 = (a·Xn + c) mod m      con a=1103515245, c=12345, m=32768
```

Este generador sustituye al módulo `random` de Python como ejercicio de implementación de generadores pseudoaleatorios.

## 📄 Licencia

Este proyecto se distribuye bajo la **Licencia MIT** (ver [LICENSE](LICENSE)). Los assets de terceros y generados por IA conservan los derechos de sus respectivos autores (ver [Atribución de assets](#-atribución-de-assets)).