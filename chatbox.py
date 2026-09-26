import pyaudiowpatch as pyaudio
import sys
sys.modules["pyaudio"] = pyaudio
import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

import speech_recognition as sr
from google import genai

client = genai.Client()

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("Calibrating for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

def listen():
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Speech service error.")
        return ""

SYSTEM_INSTRUCTION = "You are a witty, helpful assistant. Keep replies short and casual like you're talking to a friend. Don't sound too AI."

summary = ""          # summary of the old convo
recent_turns = []     # llist of last few exchanges
MAX_RECENT_TURNS = 6  # summarize after 3 exchanges

def summarize(old_summary, turns):
    turns_text = "\n".join(f"{role}: {text}" for role, text in turns)
    prompt = (
        f"Running summary so far:\n{old_summary}\n\n"
        f"Newest messages:\n{turns_text}\n\n"
        "Update the summary with the important new info. Keep it short — "
        "just key facts and context worth remembering, a few sentences max."
    )
    result = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        generation_config={"thinking_level": "low"}
    )
    return result.output_text

while True:
    user_input = listen()

    if user_input.strip() == "":
        continue
    if user_input.lower() in ["quit", "exit"]:
        break

    context_text = f"Summary of earlier conversation: {summary}\n\n" if summary else ""
    for role, text in recent_turns:
        context_text += f"{role}: {text}\n"
    context_text += f"User: {user_input}"

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        input=context_text,
        generation_config={"thinking_level": "low"}
    )

    reply = interaction.output_text
    print("Bot:", reply)
    speak(reply)

    recent_turns.append(("User", user_input))
    recent_turns.append(("Bot", reply))

    if len(recent_turns) >= MAX_RECENT_TURNS:
        summary = summarize(summary, recent_turns)
        recent_turns = []