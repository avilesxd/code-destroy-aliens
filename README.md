# 🚀 Alien Invasion
  
Welcome to the **Alien Invasion** project, a *Space Invaders*-style game developed in Python. Get ready to defend Earth!

---

## 🛠️ Start developing

### 1. Create a virtual environment

```bash
python -m venv env
```

### 2. Activate a virtual environment

- **Windows:**

```bash
env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧱 Compile the game (Windows)

### 1. Create a custom `.spec` file

```bash
pyi-makespec main.py \
--name="Alien Invasion" \
--icon="src\icons\icon.ico" \
--onefile \
--noconsole \
--add-data="src\configuration;src\configuration" \
--add-data="src\images;src\images" \
--add-data="src\music;src\music" \
--add-data="src\objects;src\objects" \
--add-data="src\utils.py;." \
--version-file="version.txt"
```

### 2. Compile the game

```bash
pyinstaller ".\Alien Invasion.spec"
```

---

## 🎮 Game Controls

- ⬅️ Left Arrow: Move left
- ➡️ Right Arrow: Move right
- 🔫 Spacebar: Shoot
- ❌ Q: Quit the game

---

## 🖼️ Game Design (early)

### 🕹️ Start Screen

![Game Start][game_start_url]

### 🧑‍🚀 Level Running

![Initial Level][game_over_url]

### ❤️ Remaining Lives and Current Score

![Game UI][high_score_url]

---

## 👨‍💻 Creators

- [@avilesxd][avilesxd_account_url]
- [@JGalaz7][jgalaz7_account_url]

---

## 🌐 Social Media

- [🐱 GitHub][github_account]
- [📸 Instagram][instagram_account]
- [📘 Facebook][facebook_account]
- [📺 YouTube][youtube_account]
- [🎵 TikTok][tiktok_account]

<!-- IMAGES -->
[game_start_url]: ./docs/README/game_start.PNG
[game_over_url]: ./docs/README/game_over.PNG
[high_score_url]: ./docs/README/high_score.PNG

<!-- CREATORS -->
[avilesxd_account_url]: http://github.com/avilesxd/
[jgalaz7_account_url]: http://github.com/JGalaz7/

<!-- SOCIAL MEDIA -->
[github_account]: http://github.com/avilesxd/
[instagram_account]: https://www.instagram.com/avilesxd/
[facebook_account]: https://www.facebook.com/ignacio.avilescardenasso
[youtube_account]: https://www.youtube.com/channel/UCYPsgamO7XeWOrXriOpJBqw
[tiktok_account]: https://www.tiktok.com/@chle_igns
