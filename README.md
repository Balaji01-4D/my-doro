<h1 align="center">MyDoro 🕰️</h1>

<div align="center">

<a href="https://github.com/Balaji01-4D/my-doro/stargazers"><img src="https://img.shields.io/github/stars/Balaji01-4D/my-doro" alt="Stars Badge"/></a>
<a href="https://github.com/Balaji01-4D/my-doro/network/members"><img src="https://img.shields.io/github/forks/Balaji01-4D/my-doro" alt="Forks Badge"/></a>
<a href="https://github.com/Balaji01-4D/my-doro/pulls"><img src="https://img.shields.io/github/issues-pr/Balaji01-4D/my-doro" alt="Pull Requests Badge"/></a>
<a href="https://github.com/Balaji01-4D/my-doro/issues"><img src="https://img.shields.io/github/issues/Balaji01-4D/my-doro" alt="Issues Badge"/></a>
<a href="https://github.com/Balaji01-4D/my-doro/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Balaji01-4D/my-doro?color=2b9348"></a>
<a href="https://github.com/Balaji01-4D/my-doro/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Balaji01-4D/my-doro?color=2b9348" alt="License Badge"/></a>

<img alt="mydoro Demo" src="img/demo.gif" />

<i>Loved the project? Please consider <a href="https://ko-fi.com/balaji01">donating</a> to help it improve!</i>

</div>

# 🕰️ MyDoro — Minimal & Colorful CLI Pomodoro Timer

Welcome to **MyDoro**! A modern, vibrant, and distraction-free Pomodoro timer for your terminal, built with Python. Boost your productivity with style! ✨

---

## 🚀 Features
- 🎨 **Colorful, modern CLI** — Enjoy a visually pleasing experience
- ⏲️ **Customizable Pomodoro & break durations**
- 🔔 **Visual & sound notifications** (if supported)
- ⚡ **Lightweight & fast**
- 🐧 **Works on Linux, macOS, and Windows**

> **Note:** If you don't hear the bell sound notifications, you may need to configure your terminal's bell sound settings. Most modern terminals allow this in their preferences or settings menu.

---

## 📦 Installation

### From PyPI

The easiest way to install MyDoro is via pip:

```sh
pip install mydoro
```

---

## 🛠️ Usage

Start your Pomodoro session from the terminal:

```sh
mydoro
```

### Command-line Arguments

Customize your Pomodoro experience with these command-line options:

```sh
# Display version information
mydoro --version

# Set custom pomodoro duration (in minutes)
mydoro --pomodoro 30

# Set custom short break duration (in minutes)
mydoro --short-break 8

# Set custom long break duration (in minutes)
mydoro --long-break 20

# Set number of cycles before a long break
mydoro --cycles 4

# Set application theme (options: dracula, monokai, github_dark, github_light)
mydoro --theme monokai

# Combine multiple options
mydoro --pomodoro 30 --short-break 8 --long-break 20 --cycles 4 --theme dracula
```

Follow the on-screen instructions and enjoy your focused work session! 💪

### Keyboard Shortcuts

MyDoro comes with convenient keyboard shortcuts for quick access to features:

| Shortcut | Action |
|----------|--------|
| <kbd>m</kbd> | Open Add Custom Duration screen |
| <kbd>Ctrl</kbd> + <kbd>p</kbd> | Open command prompt to change theme |
| <kbd>Ctrl</kbd> + <kbd>q</kbd> | Exit application |

---

## 📸 Screenshots

<div align="center">
  <!-- First row: Timer and Duration Settings -->
  <div>
    <img src="img/timer.png" alt="MyDoro Timer" style="max-width: 100%; width: 45%; min-width: 300px; margin: 10px;" />
    <img src="img/add_duration.png" alt="Add Duration Screen" style="max-width: 100%; width: 45%; min-width: 300px; margin: 10px;" />
  </div>
  <p>
    <b>Main Timer Interface</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Custom Duration Settings</b>
  </p>

  <!-- Second row: Short Breaks -->
  <div>
    <img src="img/short_break.png" alt="Short Break - Default Theme" style="max-width: 100%; width: 45%; min-width: 300px; margin: 10px;" />
    <img src="img/short_break_monokai.png" alt="Short Break - Monokai Theme" style="max-width: 100%; width: 45%; min-width: 300px; margin: 10px;" />
  </div>
  <p>
    <b>Short Break - Default Theme</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Short Break - Monokai Theme</b>
  </p>
</div>

---

## 🎛️ Customization
- Adjust Pomodoro and break durations via settings or command-line arguments (if supported)
- Explore the `mydoro/` directory for configuration options

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
MIT License — free for personal & commercial use.

---

> Made with ❤️ for productivity!
