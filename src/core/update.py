import subprocess

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
    if remoteVersion > localVersion:
        # update verfügbar
        return remoteVersion
    else:
        return ""
        

def checkForUpdates():
    """If update is found, asks user to update."""
    updateAvailable = searchForUpdates()
    if updateAvailable:
        print(f"Update auf v{updateAvailable} verfügbar!")
    else:
        print("Kein Update gefunden, deine Version ist auf dem neusten stand.")

def downloadUpdate():
    """Clones the release branch of the repository."""
    url = "https://github.com/Maxilo92/Updates.git"

    result = subprocess.run(["git", "clone", "-b", "release", url], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Klonen fehlgeschlagen: {result.stderr.strip()}")

def installUpdate():
    ...

if __name__ == "__main__":    
    updateAvailable = searchForUpdates()
    if updateAvailable:
        print(f"Update auf v{updateAvailable} verfügbar!")
    else:
        print("Kein Update gefunden, deine Version ist auf dem neusten stand.")
