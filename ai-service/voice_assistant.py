import json, os, urllib.error, urllib.request
from pathlib import Path
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr

load_dotenv(Path(__file__).resolve().with_name(".env"))
API_URL="http://127.0.0.1:8000/command"
WAKE_WORDS=("friday","fridey")
EXIT_PHRASES=("stop listening","exit assistant","goodbye friday","shutdown fridey")
OFFLINE=os.getenv("FRIDEY_OFFLINE_VOICE","false").strip().lower() in {"1","true","yes"}
VOSK_MODEL_PATH=os.getenv("VOSK_MODEL_PATH","").strip()

def speak(engine,text):
    print(f"FRIDEY: {text}"); engine.say(text); engine.runAndWait()
def ask(text):
    req=urllib.request.Request(API_URL,data=json.dumps({"text":text}).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=100) as response: return json.loads(response.read().decode())
def recognize(recognizer,audio):
    if OFFLINE:
        if not VOSK_MODEL_PATH or not os.path.isdir(VOSK_MODEL_PATH): raise RuntimeError("Offline voice enabled, but VOSK_MODEL_PATH is not a valid extracted model folder.")
        try: return recognizer.recognize_vosk(audio,model=VOSK_MODEL_PATH).strip()
        except sr.RequestError as exc: raise RuntimeError("Offline recognition requires pip install vosk and a downloaded model.") from exc
    return recognizer.recognize_google(audio,language="en-IN").strip()
def main():
    r=sr.Recognizer(); r.pause_threshold=.8; mic=sr.Microphone(); t=pyttsx3.init(); t.setProperty("rate",170)
    print("FRIDEY voice ready ("+("offline Vosk" if OFFLINE else "online Google")+"). Say Friday/Fridey.")
    with mic as source: r.adjust_for_ambient_noise(source,duration=1)
    while True:
        try:
            with mic as source: audio=r.listen(source,timeout=5,phrase_time_limit=12)
            heard=recognize(r,audio); print("You:",heard); low=heard.casefold()
            if any(x in low for x in EXIT_PHRASES): speak(t,"Okay. FRIDEY is going offline."); break
            index=next((low.find(w) for w in WAKE_WORDS if w in low),-1)
            if index<0: continue
            tail=heard[index:]
            for w in WAKE_WORDS:
                if tail.casefold().startswith(w): tail=tail[len(w):]; break
            command=tail.strip(" ,.!?")
            speak(t,"Yes, I am listening.")
            if not command:
                with mic as source: command=recognize(r,r.listen(source,timeout=8,phrase_time_limit=15))
            try: speak(t,ask(command).get("reply","I did not receive a reply."))
            except (urllib.error.URLError,TimeoutError,ValueError) as exc: print("API error:",exc); speak(t,"I cannot reach my AI service. Start FRIDEY's API.")
        except (sr.WaitTimeoutError,sr.UnknownValueError): continue
        except sr.RequestError as exc: print(exc); speak(t,"Speech recognition is unavailable.")
        except RuntimeError as exc: print(exc); speak(t,str(exc)); break
        except KeyboardInterrupt: print("FRIDEY stopped."); break
if __name__=="__main__": main()
