# 🚀 Code Destroy the Aliens

Welcome to the **Code Destroy the Aliens** project, a *Space Invaders*-style game developed in Python. Get ready to defend Earth!

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
--name="Destroy Aliens" \
--icon="src\imagenes\icono.ico" \
--onefile \
--noconsole \
--add-data="src\configuracion;src\configuracion" \
--add-data="src\images;src\images" \
--add-data="src\music;src\music" \
--add-data="src\objects;src\objects" \
--add-data="src\utils.py;src" \
--version-file="version.txt"
```

### 2. Compile the game

```bash
pyinstaller ".\Destroy Aliens.spec"
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

![Game Start](./docs/README/foto1.PNG)

### 🧑‍🚀 Level Running

![Initial Level](./docs/README/foto2.PNG)

### ❤️ Remaining Lives and Current Score

![Game UI](./docs/README/foto3.PNG)

---

## 👨‍💻 Creators

- **Ignacio Avilés**
- **Juan Galaz**

---

## 🌐 Social Media

- [🐱 GitHub](http://github.com/avilesxd/)
- [📸 Instagram](https://www.instagram.com/avilesxd/)
- [📘 Facebook](https://www.facebook.com/ignacio.avilescardenasso)
- [📺 YouTube](https://www.youtube.com/channel/UCYPsgamO7XeWOrXriOpJBqw)
- [🎵 TikTok](https://www.tiktok.com/@chle_igns)
