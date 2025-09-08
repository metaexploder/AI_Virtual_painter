
# 🎨 AI Virtual Painter

AI Virtual Painter is a fun and interactive application that lets you draw, erase, fill, and create different shapes on a virtual canvas — **using only your hand gestures**!
It uses your webcam to track your hand movements in real-time with **MediaPipe** and **OpenCV**, making it completely hands-free.

---

## ✨ Features

- 🖌️ **Freestyle Drawing** – Use your index finger to draw freely on the canvas.
- 📐 **Shape Drawing** – Draw **rectangles**, **circles**, **triangles**, **stars**, and **arrows** using gestures.
- 🧹 **Eraser Tool** – Erase parts of your drawing by simply pointing at them.
- 🪄 **Fill Tool** – Instantly fill shapes or areas with your selected color.
- 🎨 **Color Palette** – Choose from 6 pre-defined colors to make your drawings creative.
- 👆 **Gesture-Based Controls** – No mouse or keyboard needed, just your hand!
- ⚡ **Real-Time Processing** – Smooth and fast performance powered by OpenCV and MediaPipe.

---

## 🛠️ Tech Stack

- **Language:** Python 🐍
- **Computer Vision:** OpenCV
- **Hand Tracking:** MediaPipe
- **Array & Shape Handling:** NumPy

---

## 📂 Project Structure

AI-Virtual-Painter/
│── main.py            # Main file to start the app
│── hand_tracker.py    # Handles hand detection & finger tracking
│── painter.py         # Drawing, filling, shapes & canvas logic
│── ui.py              # UI for color palette, modes & shapes
│── requirements.txt   # Project dependencies
│── README.md          # Project documentation
│── assets/            # (Optional) Screenshots, demo GIFs, etc.

---

## 🚀 Installation & Setup

Follow these steps to run the project on your system:

### 1️⃣ Clone the Repository
git clone https://github.com/<your-username>/AI-Virtual-Painter.git
cd AI-Virtual-Painter

### 2️⃣ Install Dependencies
Make sure you have **Python 3.8+** installed, then run:
pip install -r requirements.txt

### 3️⃣ Run the Application
python main.py

---

## 🎮 How to Use

| **Gesture / Key**          | **Action**                              |
|----------------------------|---------------------------------------|
| Index finger up           | Draw freely on the canvas            |
| Index + middle finger up  | Select colors, shapes, or modes      |
| Tap index finger on mode  | Switch between freestyle, shapes, eraser, fill, etc. |
| Tap index finger on color | Change drawing color                |
| Hold index finger on canvas | Start drawing shapes               |
| Move two fingers apart    | Resize shapes dynamically           |
| Index finger in eraser mode | Erase drawings                    |
| **Press `C`**             | Clear the entire canvas            |
| **Press `Q`**             | Quit the application               |

---

## 🖼️ Drawing Modes

- ✏️ Freestyle Drawing
- 📐 Shape Drawing
- 🧹 Eraser Mode
- ✕ Clear Shape
- ◉ Fill Shape

### **Shapes You Can Draw**
- ▢ Rectangle
- ○ Circle
- △ Triangle
- ★ Star
- → Arrow

---

## 🧠 How It Works

1. **Hand Tracking** → Uses **MediaPipe Hands** to detect and track 21 hand landmarks in real-time.
2. **Gesture Recognition** → Detects whether your **index** or **middle** fingers are up and maps them to actions.
3. **Drawing Logic** →
   - One finger = draw
   - Two fingers = select tools, shapes, or colors
   - Dragging gestures = resizing shapes.
4. **Virtual Canvas** → Uses OpenCV to combine live video feed and canvas drawings smoothly.

---

## 📸 Demo

*(You can add screenshots or a demo GIF here once ready)*

---

## 👨‍💻 Author

**Vishal**
[GitHub](https://github.com/<your-username>)

---

## 📜 License

This project is open-source and available under the **MIT License**.
