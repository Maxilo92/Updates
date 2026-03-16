import subprocess

def getRemoteVersion():
    # Nutze die 'raw' URL und trenne die Argumente in einer Liste
    url = "https://raw.githubusercontent.com/Maxilo92/Updates/main/VERSION"
    
    result = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    
    if result.returncode == 0:
        VERSION = result.stdout.strip()
        # print(f"Aktuelle Version: {VERSION}")
        return VERSION
    else:
        print("Fehler beim Abrufen der Version.")
        return "0.0.0"


def checkForUpdates():
    print(getRemoteVersion())

checkForUpdates()