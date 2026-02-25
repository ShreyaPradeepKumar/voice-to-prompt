# 🎙️ Voice to Prompt Converter

Convert your voice (in **English** or **Hindi**) into professional, AI-ready prompts using speech recognition and AI enhancement.

## ✨ Features

- 🎤 **Voice Input**: Speak naturally in English or Hindi
- 🌍 **Automatic Translation**: Hindi to English translation
- 🤖 **AI Enhancement**: Converts casual speech to structured prompts using GPT-4
- 💻 **Two Interfaces**: 
  - Command-line interface (`main.py`)
  - Web interface with Streamlit (`app.py`)

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- A microphone
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 2. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

**Note for Windows users**: If PyAudio installation fails, download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it manually:
```bash
pip install PyAudio-0.2.11-cp3xx-cp3xx-win_amd64.whl
```

### 3. Configuration

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 🎯 Usage

### Option 1: Command Line Interface

```bash
python main.py
```

This will:
1. Listen to your voice
2. Detect language (English/Hindi)
3. Translate if needed
4. Generate an AI-ready prompt

### Option 2: Web Interface (Streamlit)

```bash
streamlit run app.py
```

Then open your browser to the displayed URL (usually `http://localhost:8501`)

Features:
- Adjustable recording duration
- Language selection
- Visual feedback
- Easy copy of generated prompts

## 📝 Example

**You speak (Hindi):**  
> "मुझे एक ऐसा प्रोग्राम चाहिए जो दो नंबरों को जोड़ सके"

**Output:**
```
Original Text (Hindi): मुझे एक ऐसा प्रोग्राम चाहिए जो दो नंबरों को जोड़ सके
Translated to English: I need a program that can add two numbers
AI-Ready Prompt: Create a Python program that takes two numbers as input and returns their sum.
```

## 🛠️ Troubleshooting

### Microphone not detected
- Ensure your microphone is connected
- Check system permissions for microphone access
- On Windows, go to Settings > Privacy > Microphone

### "Could not understand audio"
- Speak clearly in a quiet environment
- Increase the recording duration
- Check microphone volume levels

### PyAudio installation errors
- On Windows: Download pre-built wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- On macOS: `brew install portaudio` then `pip install pyaudio`
- On Linux: `sudo apt-get install python3-pyaudio`

## 📦 Dependencies

- `speechrecognition` - Voice recognition
- `deep-translator` - Translation (Hindi ↔ English)
- `openai` - AI prompt enhancement
- `streamlit` - Web interface
- `pyaudio` - Microphone access
- `python-dotenv` - Environment variable management

## 🔒 Security Note

Never commit your `.env` file with your actual API key. The `.env` file is gitignored for security.

## 📄 License

MIT License - Feel free to use and modify!

---

Made with ❤️ for seamless voice-to-prompt conversion