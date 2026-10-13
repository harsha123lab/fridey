"""Allowlisted Windows actions. Never run arbitrary model-generated commands."""
import os
import re
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path


def _open_app(name: str) -> str:
    apps = {
        "chrome": ["cmd", "/c", "start", "", "chrome"],
        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"],
        "vscode": ["cmd", "/c", "start", "", "code"],
        "file explorer": ["explorer.exe"],
        "explorer": ["explorer.exe"],
    }
    command = apps.get(name)
    if not command:
        return ""
    try:
        subprocess.Popen(command, shell=False)
        return f"Opened {name}."
    except (OSError, subprocess.SubprocessError):
        if name == "chrome":
            try:
                webbrowser.open("https://www.google.com")
                return "Opened your default browser because Chrome was not found."
            except Exception:
                pass
        return f"I couldn't open {name}. Check whether it is installed."


def handle_desktop_command(text: str) -> dict | None:
    clean = re.sub(r"\s+", " ", text.strip())
    lower = clean.casefold()
    if lower in {"open downloads", "open my downloads", "downloads folder"}:
        path = Path.home() / "Downloads"
        if path.exists():
            os.startfile(str(path))
            return {"action": "open_folder", "reply": "Opened your Downloads folder."}
        return {"action": "open_folder", "reply": "I couldn't find your Downloads folder."}

    patterns = [
        (r"^(?:please )?(?:open|launch|start) (?:google )?chrome$", "chrome"),
        (r"^(?:please )?(?:open|launch|start) notepad$", "notepad"),
        (r"^(?:please )?(?:open|launch|start) (?:the )?calculator$", "calculator"),
        (r"^(?:please )?(?:open|launch|start) (?:vs code|visual studio code|vscode)$", "vscode"),
        (r"^(?:please )?(?:open|launch) (?:file explorer|explorer)$", "file explorer"),
    ]
    for pattern, app in patterns:
        if re.match(pattern, lower):
            return {"action": "open_app", "reply": _open_app(app)}
    if lower in {"open youtube", "launch youtube"}:
        webbrowser.open("https://www.youtube.com")
        return {"action": "open_website", "reply": "Opened YouTube."}
    match = re.match(r"^(?:play|search youtube for|youtube search) (.+)$", clean, re.I)
    if match:
        query = urllib.parse.quote_plus(match.group(1))
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return {"action": "youtube_search", "reply": f"Opened YouTube results for {match.group(1)}."}
    match = re.match(r"^(?:search google for|google search|search the web for) (.+)$", clean, re.I)
    if match:
        query = urllib.parse.quote_plus(match.group(1))
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return {"action": "web_search", "reply": f"Opened Google results for {match.group(1)}."}
    match = re.match(r"^(?:open website|go to) (.+)$", clean, re.I)
    if match:
        target = match.group(1).strip()
        if re.fullmatch(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[^ ]*)?", target):
            webbrowser.open("https://" + target)
            return {"action": "open_website", "reply": f"Opened {target}."}
    match = re.match(r"^type this:\s*(.{1,500})$", clean, re.I)
    if match:
        try:
            import pyautogui
            pyautogui.write(match.group(1), interval=0.01)
            return {"action": "type_text", "reply": "Typed the requested text into the currently focused window."}
        except Exception:
            return {"action": "type_text", "reply": "I couldn't type the text. Focus the target window and check PyAutoGUI permissions."}
    return None
