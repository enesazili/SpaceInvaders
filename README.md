# 👾 Space Invaders

A retro-inspired arcade shooter built with **Python** and **Pygame**. Take on waves of enemies in a project inspired by the classic Space Invaders gameplay.

## ✨ Features

- Space Invaders-inspired arcade gameplay
- Python and Pygame implementation
- Dockerized environment for easier setup and reproducibility

## 🛠️ Tech Stack

- Python
- Pygame
- Docker

## 🚀 Getting Started

### Run with Docker

Build the image:

```bash
docker build -t spaceinvaders-game .
```

Run the game:

```bash
docker run -it --rm spaceinvaders-game
```

> **Note:** Pygame requires graphical display support. Running the game inside Docker may require display forwarding or another GUI configuration appropriate for your operating system.
