import os
import sys
import shutil
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def getRemoteVersion():
    """curl's the version from VERSION of Github and returns it"""
    url = "https://raw.githubusercontent.com/Maxilo92/Updates/main/VERSION"
    
    # print("suche nach updates...")
    result = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    
    if result.returncode == 0:
        VERSION = result.stdout.strip()
        # print(f"Aktuelle Version: {VERSION}")
        return VERSION
    else:
        print("Fehler beim Abrufen der Version.")
        return "0.0.0"
    
def getLocalVersion():
    """Reads the version from local VERSION and returns it"""
    try:
        f = open("VERSION")
        v = f.readline()
    except:
        raise(FileNotFoundError("VERSION fehlt oder ist beschädigt"))
    finally:
        f.close()
    return v


def searchForUpdates():
    """Compares the local and remote version. Returns remote version if newer, else empty str."""
    remoteVersion = getRemoteVersion()
    localVersion = getLocalVersion()

    print(f"remote: {remoteVersion}; local: {localVersion}")
    if remoteVersion.strip() > localVersion.strip():
        # update verfügbar
        return remoteVersion
    else:
        return ""
        

def checkForUpdates():
    """If update is found, asks user to update."""
    updateAvailable = searchForUpdates()
    if updateAvailable:
        print(f"Update auf v{updateAvailable} verfügbar!")
        choice = input(f"Auf v{updateAvailable} upgraden? (y/n): ").strip().lower()
        if choice == "y":
            initUpdate()

    else:
        print("Kein Update gefunden, deine Version ist auf dem neusten stand.")

def downloadUpdate():
    """Clones the release branch of the repository."""
    url = "https://github.com/Maxilo92/Updates.git"
    destination = f"./.update-{getRemoteVersion()}"

    result = subprocess.run(["git", "clone", "-b", "release", url, destination], capture_output=True, text=True)
    if result.returncode != 0:
        print("Update bereits heruntergeladen.")
        # raise RuntimeError(f"Klonen fehlgeschlagen: {result.stderr.strip()}")
    print(f"Update wurde nach '{destination}' geklont.")

    return destination

def installUpdate(new_version_path):
    # Inhalte des geklonten Repos in das Projektverzeichnis kopieren.
    for entry in os.listdir(new_version_path):
        if entry == ".git":
            continue

        src = os.path.join(new_version_path, entry)
        dst = os.path.join(PROJECT_ROOT, entry)

        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    shutil.rmtree(new_version_path, ignore_errors=True)

    # Script neu starten (ersetzt den aktuellen Prozess)
    os.execv(sys.executable, [sys.executable] + sys.argv)

    # Aufruf, sobald der Download von .update-0.0.2 fertig ist:
    # finalize_update('.update-0.0.2')

def initUpdate():
    updateDir = downloadUpdate()
    installUpdate(updateDir)


if __name__ == "__main__":    
    updateAvailable = searchForUpdates()
    if updateAvailable:
        print(f"Update auf v{updateAvailable} verfügbar!")
    else:
        print("Kein Update gefunden, deine Version ist auf dem neusten stand.")
