import subprocess
import os
import platform
import time
import psutil

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class Starting:
    def __init__(self) -> None:
        self.process = None

    def start_mobsf(self):
        print(f"{GREEN}[*]{RESET} Finding MobSF dir path")
        mobsf_dir_path=''
        run_script = ''
        for root, dirs, files in os.walk('/Users'):
            if 'Mobile-Security-Framework-MobSF-master' in dirs:
                mobsf_dir_path = os.path.join(root,'Mobile-Security-Framework-MobSF-master') + '/'
                if mobsf_dir_path != '':
                    break        
        if platform.system()=='Windows':
            run_script='run.bat'
        elif platform.system()=='Darwin':
            run_script='run.sh'
        if not os.path.exists(mobsf_dir_path+run_script):
            print(f"{RED}[-]{RESET} Error: The {run_script} is not in this path {mobsf_dir_path}")
            return
        self.process = subprocess.Popen(mobsf_dir_path+run_script,shell=True,cwd=mobsf_dir_path)
        print(f'{BLUE}[+]{RESET} MobSF Started Successfully')        
        return self.process

    def kill_mobsf(self):
        print(f'{GREEN}[*]{RESET} Terminating MobSF')
        if self.process and self.process.poll() is None:
            parent = psutil.Process(self.process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            self.process.terminate()
            self.process.wait()
        print(f"{GREEN}[*]{RESET} Byebye~")



