# voice chatbot 🎙️🤖

a chatbot i built while yelling WOOOOO at my terminal — currently 90% vibes, 10% chatbot, with dreams of one day controlling my laptop.

## what it does

- talks back using Gemini (`gemini-3.8-flash`)
- listens through your mic (speech-to-text) and replies out loud (text-to-speech)
- remembers the conversation using rolling summarization instead of resending the whole history (so it doesn't eat tokens for breakfast)
- can call tools to actually *do* things (starting with opening apps)

## tech stack

- Python
- `google-genai` — Gemini API (Interactions API)
- `speech_recognition` + `pyaudiowpatch` — voice input
- `pyttsx3` — voice output (offline TTS)

## setup

1. Install dependencies:
   ```
   pip install google-genai speech_recognition pyaudiowpatch pyttsx3
   ```
2. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/)
3. Set it as an environment variable:
   ```
   setx GEMINI_API_KEY "your_key_here"
   ```
4. Run it:
   ```
   python chatbox.py
   ```
5. Talk. Say "quit" or "exit" to stop.

## roadmap

- [x] basic text chatbot
- [x] conversation memory (via rolling summarization)
- [x] voice input/output
- [ ] tool calling (open apps, run scripts)
- [ ] full laptop control (mouse/keyboard/screen) — the scary one

## notes

built as a learning project, not production-grade. expect bugs, weird pauses, and the occasional robotic voice glitch.
