from core.update import checkForUpdates

def getCurVersion():
    try:
        f = open("VERSION")
        v = f.readline()
    except:
        raise(FileNotFoundError("VERSION fehlt oder ist beschädigt"))
    finally:
        f.close()
    return v

def main():
    VERSION = getCurVersion()
    print(f"Willkommen in Test App v{VERSION}")
