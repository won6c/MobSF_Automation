from startMobSF import *
from mobSFRestAPI import *
from repackagingApk import *
from key import *
from colors import *
from emulator import *
import os

def main():
    file_name = 'newapp.apk'
    device = 'android'
    de_key = b'dbcdcfghijklmaop'
    server = 'http://127.0.0.1:8000'
    emulator_name = 'Pixel_5_API_25'
    currnet = os.getcwd()

    apkPath = input(f'{BLUE}[*]{RESET} {YELLOW}Please enter the path of apk to analyze{RESET} : ')
    currnetPath = os.getcwd()
    mobsf = Starting()
    mobsf.start_mobsf()
    api_key = key()
    pack = packaging(key=de_key,file_name=file_name)
    pack.process(path=apkPath)
    emulate = emulator(emulator_name,currnet,f'{pack.find_sdk_directory()}')
    emulate.start_emulator()
    static = Analysis(server,currnetPath,apkPath,file_name,api_key.api_key(),device)
    static.Analysis()
    mobsf.kill_mobsf()
    emulate.stop_emulator()

if __name__=="__main__":
    main()