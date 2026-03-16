import os
import sys
import shutil
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def getRemoteVersion():
    """curl's the version from VERSION of Github and returns it"""
    url = "https://raw.githubusercontent.com/Maxilo92/Updates/release/VERSION"
    
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
    version_path = os.path.join(PROJECT_ROOT, "VERSION")
    try:
        with open(version_path) as f:
            return f.readline().strip()
    except FileNotFoundError:
        raise FileNotFoundError("VERSION fehlt oder ist beschädigt")


def compareVersions(v1, v2):
    """Compares semantic versions like 0.0.3. Returns 1, 0, -1."""
    def parse(v):
        parts = v.strip().split(".")
        return tuple(int(p) for p in parts)

    a = parse(v1)
    b = parse(v2)

    if a > b:
        return 1
    if a < b:
        return -1
    return 0


def searchForUpdates():
    """Compares the local and remote version. Returns remote version if newer, else empty str."""
    remoteVersion = getRemoteVersion()
    localVersion = getLocalVersion()

    print(f"remote: {remoteVersion}; local: {localVersion}")
    if compareVersions(remoteVersion, localVersion) > 0:
        # update verfügbar
        return remoteVersion
    else:
        return ""
        

def checkForUpdates():
    """If update is found, asks user to update."""
    remoteVersion = getRemoteVersion()
    localVersion = getLocalVersion()
    versionCmp = compareVersions(remoteVersion, localVersion)

    print(f"remote: {remoteVersion}; local: {localVersion}")
    if versionCmp > 0:
        print(f"Update auf v{remoteVersion} verfügbar!")
        choice = input(f"Auf v{remoteVersion} upgraden? (y/n): ").strip().lower()
        if choice == "y":
            initUpdate()
    elif versionCmp < 0:
        print("Update release")
    else:
        print("Kein Update gefunden, deine Version ist auf dem neusten stand.")

def downloadUpdate():
    """Clones the release branch of the repository."""
    url = "https://github.com/Maxilo92/Updates.git"
    destination = os.path.join(PROJECT_ROOT, f".update-{getRemoteVersion()}")

    if os.path.exists(destination):
        print(f"Update bereits heruntergeladen.")
    else:
        result = subprocess.run(["git", "clone", "-b", "release", url, destination], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Klonen fehlgeschlagen: {result.stderr.strip()}")
    print(f"Update wurde nach '{destination}' geklont.")
    return destination

def installUpdate(new_version_path):
    """Copies files from the cloned update into PROJECT_ROOT, then restarts."""
    for entry in os.listdir(new_version_path):
        if entry in (".git",):
            continue
        src = os.path.join(new_version_path, entry)
        dst = os.path.join(PROJECT_ROOT, entry)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    shutil.rmtree(new_version_path, ignore_errors=True)
    os.execv(sys.executable, [sys.executable] + sys.argv)

def initUpdate():
    updateDir = downloadUpdate()
    installUpdate(updateDir)

if __name__ == "__main__":    
    updateAvailable = searchForUpdates()
    if updateAvailable:
        print(f"Update auf v{updateAvailable} verfügbar!")
    else:
        print("Kein Update gefunden, deine Version ist auf dem neusten stand.")
