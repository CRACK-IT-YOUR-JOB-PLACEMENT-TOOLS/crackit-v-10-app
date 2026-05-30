# 🚀 CrackIt! - Your Ultimate Interview Assistant

CrackIt! is a stealthy, background-running assistant designed to help you ace your online assessments and interviews. With a draggable traffic-light indicator, fast keyboard shortcuts, and intelligent clipboard monitoring, you can get the best answers to interview questions in seconds without ever breaking focus or leaving your screen.

## ✨ Features

- **🚥 Traffic Light Indicator:** A minimalist floating dot indicating status (🔴 Waiting, 🟡 Processing, 🟢 Ready).
- **🥷 Stealth Mode:** Hide the tool instantly when sharing your screen.
- **⚡ Auto-Copy & Process:** Quickly grab questions with a shortcut to generate the best answer using AI.
- **⌨️ Auto-Typer:** Bypass copy-paste blocks by having the assistant naturally type the answer out for you.
- **🧠 NVIDIA NIM Powered:** Generates highly accurate answers fast.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.8+**
- An **NVIDIA NIM API Key** ([Get one here](https://build.nvidia.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/CRACK-IT-YOUR-JOB-PLACEMENT-TOOLS/crackit-v-10-app.git
cd crackit-v-10-app
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to create your `.env` configuration. You can also configure this within the app UI upon launching.
```bash
cp .env.example .env
```
Edit `.env` and add your NVIDIA API Key:
```env
NVIDIA_API_KEY="your_nvidia_api_key_here"
```

---

## 🚀 Running the App

Start the assistant by running:
```bash
python main.py
```

### First Launch
On the first launch, you will be greeted with a setup window. Enter your **NVIDIA NIM API Key** and click **Save & Start**. The assistant will minimize into a floating red dot on your screen. 

*(Note: The app will automatically configure itself to start with Windows if allowed!)*

---

## 🎮 How to Use (Gestures & Shortcuts)

- **`Alt+C` (Auto-Copy):** Highlight any interview question and press `Alt+C`. The indicator turns **Yellow** (Processing) and then **Green** (Ready), copying the best answer to your clipboard.
- **`Alt+V` (Auto-Typer):** Simulates fast typing of the generated answer to bypass strict paste blocks.
- **`Alt+1` (Stealth Mode):** Instantly hides or shows the traffic light dot.
- **Long Press on Red Dot:** Displays the setup dialog to reconfigure your API key.
- **Double Tap on Green Dot:** Resets the app back to Red (waiting state).
- **Long Press on Green Dot:** Immediately stops and closes the app safely.

---

## ⚠️ Disclaimer
This tool is for educational purposes and personal preparation only. Use responsibly and ethically during your interviews and assessments.
