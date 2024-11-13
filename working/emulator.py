import subprocess
import os
from colors import *

class emulator:
    def __init__(self,name,current,path) -> None:
        self.name = name
        self.current = current
        self.emulator_path = path+'/../../emulator'

    def start_emulator(self):
        os.chdir(self.emulator_path)
        print(f"{BLUE}[*]{RESET} Starting the Emulator {self.name}")

        command = f"tell application \"Terminal\" to do script \"cd {self.emulator_path} && ./emulator -avd {self.name} -writable-system -no-snapshot\""
        subprocess.run(["osascript", "-e", command])

        os.chdir(self.current)

    def stop_emulator(self):
        print(f"{RED}[*]{RESET} Stopping the Emulator {self.name}")
        subprocess.run(["pkill", "-f", "emulator"])
