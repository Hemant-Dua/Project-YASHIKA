import os
import subprocess

# Map app keywords to commands or paths
APP_COMMANDS = {
    "vs code": "code",
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "youtube": r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://youtube.com',
    "github": r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://github.com/Hemant-Dua',
    "chess": r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.chess.com/home',
    "codeforces": r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://codeforces.com/problemset?order=BY_RATING_ASC',
    "chatgpt": r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://chatgpt.com/',
    "cmd": "start cmd",
    "powershell": "start powershell",
    "task manager": "taskmgr",
    "explorer": "explorer",
    "snipping tool": "snippingtool",
    "paint": "mspaint",
    "settings": "start ms-settings:",
}

GAME_TRIGGERS = {
    "valorant": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\VALORANT.lnk",
    "gta trilogy": r"D:\Games\GTA - The Trilogy - DE\Launcher.exe"
}

# Map folder keywords to absolute paths
FOLDER_PATHS = {
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "desktop": os.path.expanduser("~/Desktop"),
    "pictures": os.path.expanduser("~/Pictures"),
    "videos": os.path.expanduser("~/Videos"),
    "music": os.path.expanduser("~/Music"),
    "projects": "E:",  # Custom project folder
    "this pc": "C:\\"
}

# yashika_actions.py
def handle_local_commands(user_input: str) -> tuple[str | None, bool]:
    lowered = user_input.lower()

    for name, cmd in APP_COMMANDS.items():
        if f"open {name}" in lowered:
            subprocess.Popen(cmd, shell=True)
            return (f"Opening {name}...", True)

    for name, path in FOLDER_PATHS.items():
        if f"open {name}" in lowered or f"show {name}" in lowered:
            os.startfile(path)
            return (f"Opening {name} folder...", True)
        
    for name, path in GAME_TRIGGERS.items():
        if f"open {name}" in lowered or f"play {name}" in lowered:
            os.startfile(path)
            return (f"Starting {name}...", True)

    return (None, False)

