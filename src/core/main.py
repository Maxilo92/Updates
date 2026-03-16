from core.update import checkForUpdates,getLocalVersion




def main():
    VERSION = getLocalVersion()
    print(f"Willkommen in Test App v{VERSION}")

    checkForUpdates()
  
