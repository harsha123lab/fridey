"""FRIDEY Windows app launcher. Bundles the API and optional voice client."""
import argparse
import os
import shutil
import sys
import threading
import time
import webbrowser
from pathlib import Path

APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
LOCAL_ROOT = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
USER_DIR = LOCAL_ROOT / "FRIDEY"
USER_DIR.mkdir(parents=True, exist_ok=True)
ENV_FILE = USER_DIR / ".env"
if not ENV_FILE.exists():
    template = APP_DIR / ".env.example"
    if template.exists():
        shutil.copyfile(template, ENV_FILE)

# Settings and SQLite data must live outside Program Files / the bundled executable.
os.environ.setdefault("FRIDEY_DATA_DIR", str(USER_DIR / "data"))
os.environ.setdefault("FRIDEY_ENV_FILE", str(ENV_FILE))
from dotenv import load_dotenv
load_dotenv(ENV_FILE, override=False)
os.chdir(USER_DIR)
sys.path.insert(0, str(APP_DIR))


def start_api():
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


def main():
    parser = argparse.ArgumentParser(description="FRIDEY personal AI assistant")
    parser.add_argument("--voice", action="store_true", help="Start the voice assistant")
    args = parser.parse_args()

    if args.voice:
        server = threading.Thread(target=start_api, daemon=True, name="fridey-api")
        server.start()
        time.sleep(1.5)
        from voice_assistant import main as voice_main
        voice_main()
        return

    threading.Timer(1.3, lambda: webbrowser.open("http://127.0.0.1:8000/dashboard")).start()
    start_api()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
