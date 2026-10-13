import json
import urllib.error
import urllib.request
import pyttsx3
import speech_recognition as sr

API_URL = "http://127.0.0.1:8000/command"
WAKE_WORDS = ("friday", "fridey")
EXIT_PHRASES = ("stop listening", "exit assistant", "goodbye friday", "shutdown fridey")


def speak(engine, text: str) -> None:
    print(f"FRIDEY: {text}")
    engine.say(text)
    engine.runAndWait()


def ask_friday(text: str) -> dict:
    payload = json.dumps({"text": text}).encode("utf-8")
    request = urllib.request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=100) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    print("FRIDEY voice is ready. Say Friday or Fridey to wake it. Say stop listening to exit.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    while True:
        try:
            with microphone as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=12)
            heard = recognizer.recognize_google(audio, language="en-IN").strip()
            print(f"You: {heard}")
            lower = heard.casefold()
            if any(phrase in lower for phrase in EXIT_PHRASES):
                speak(engine, "Okay. FRIDEY is going offline.")
                break
            wake_index = next((lower.find(word) for word in WAKE_WORDS if word in lower), -1)
            if wake_index < 0:
                continue
            remainder = heard[wake_index:]
            for word in WAKE_WORDS:
                if remainder.casefold().startswith(word):
                    remainder = remainder[len(word):]
                    break
            command_text = remainder.strip(" ,.!?")
            speak(engine, "Yes, I am listening.")
            if not command_text:
                with microphone as source:
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
                command_text = recognizer.recognize_google(audio, language="en-IN").strip()
                print(f"You: {command_text}")
            try:
                result = ask_friday(command_text)
                speak(engine, result.get("reply", "I did not receive a reply."))
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                print(f"API error: {exc}")
                speak(engine, "I cannot reach my AI service. Please start FRIDEY's API.")
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except sr.RequestError as exc:
            print(f"Speech recognition error: {exc}")
            speak(engine, "Speech recognition is unavailable right now.")
        except KeyboardInterrupt:
            print("FRIDEY stopped.")
            break


if __name__ == "__main__":
    main()
