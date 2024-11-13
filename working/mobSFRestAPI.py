import requests
import os
import json
from datetime import datetime
from requests_toolbelt import MultipartEncoder
from colors import *

class Analysis:
    def __init__(self,server,file_path,file_name,api_key,device) -> None:
        self.server = server
        self.path = file_path
        self.file_path = file_path+'/'+file_name
        self.api_key=api_key
        self.scan_hash=''
        self.device=device

    def upload_apk(self):
        print(f'{BLUE}[*]{RESET} Uploading APK')
        multipart_data = MultipartEncoder(
            fields = {'file':(self.file_path, open(self.file_path,'rb'),'application/octet-stream')}
        )
        headers = {
            'Content-Type':multipart_data.content_type,
            'Authorization':self.api_key
        }
        response = requests.post(f'{self.server}/api/v1/upload',data=multipart_data, headers=headers)
        result = response.json()
        if 'hash' in result:
            self.scan_hash = result['hash']
            print(f'{GREEN}[+]{RESET} Upload completed')

    def scan_apk(self):
        print(f'{BLUE}[*]{RESET} Scanning Started')
        data = {
            'hash':self.scan_hash,
            'scan_type':self.file_path.split('.')[-1],
            'file_name':os.path.basename(self.file_path)
            }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f'{self.server}/api/v1/scan',data=data,headers=headers)
        print(f'{GREEN}[+]{RESET} Scanning completed')

    def static_json(self):
        print(f"{BLUE}[*]{RESET} Generating Static json")
        data = {
            "hash":self.scan_hash
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/report_json",data=data,headers=headers)
        date = datetime.now().strftime("%Y-%m-%d")
        with open(self.path+f'/static_report-{date}.json','w+') as f:
            json.dump(response.json(),f)
        return response

    def download_pdf(self):
        print(f'{BLUE}[*]{RESET} Downloading the pdf')
        data = {
            'hash':self.scan_hash,
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f'{self.server}/api/v1/download_pdf',data=data,headers=headers)
        date = datetime.now().strftime("%Y-%m-%d")
        with open(self.path+f'/static_analysis_report-{date}.pdf','wb') as f:
            f.write(response.content)
        print(f'{GREEN}[+]{RESET} Download complete')
        print(f'{BLUE}[*]{RESET} Result of static analyze is at {YELLOW}{self.path+"/static_analysis_report.pdf"}{RESET}')

    def delete(self):
        print(f"{BLUE}[*]{RESET} Deleting")
        data = {
            "hash":self.scan_hash
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/delete_scan",data=data,headers=headers)
        return response
    


    def get_apps(self):
        print(f"{BLUE}[*]{RESET} Connecting to Emulator")
        headers = {
            'Authorization':self.api_key
        }
        response = requests.get(f"{self.server}/api/v1/dynamic/get_apps",headers=headers)
        return response

    def start_dynamic_analysis(self):
        print(f"{BLUE}[*]{RESET} Starting Dynamic Analysis")
        data = {
            "hash":self.scan_hash
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/dynamic/start_analysis",data=data,headers=headers)
        return response

    def stop_dynamic_analysis(self):
        print(f"{BLUE}[*]{RESET} Stop Dynamic Analysis")
        data = {
            "hash":self.scan_hash
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/dynamic/stop_analysis",data=data,headers=headers)
        return response

    def dynamic_report_json(self):
        print(f"{BLUE}[*]{RESET} Making Dynamic json report")
        data = {
            "hash":self.scan_hash
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/dynamic/report_json",data=data,headers=headers)
        date = datetime.now().strftime("%Y-%m-%d")
        with open(self.path+f'/dynamic_report-{date}.json','w+') as f:
            json.dump(response.json(),f)
        return response
    
    def dynamic_act_tester(self, test):
        print(f"{BLUE}[*]{RESET} Dynamic Act Tester {test}")
        data = {
            "hash":self.scan_hash,
            "test":test
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/android/activity",data=data,headers=headers)
        return response
    
    def dynamic_start_activity(self,activity):
        print(f"{BLUE}[*]{RESET} Dynamic Start Activiry")
        data = {
            "hash":self.scan_hash,
            "activity":activity
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/android/start_activity",data=data,headers=headers)
        return response
    
    def dynamic_tls_test(self):
        print(f"{BLUE}[*]{RESET} Dynamic TLS Test")
        data = {
            "hash":self.scan_hash
        }
        headers = {
            "Authorization":self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/android/tls_tests",data=data,headers=headers)
        return response
    
    def frida_instrument(self,default_hooks='',auxiliary_hooks='',frida_code='',class_name=None,class_search=None,class_trace=None):
        data = {
            'hash':self.scan_hash,
            'default_hooks':default_hooks,
            'auxiliary_hooks':auxiliary_hooks,
            'frida_code':frida_code
        }
        if class_name:
            data['class_name']=class_name
        if class_search:
            data['class_search']=class_search
        if class_trace:
            data['class_trace']=class_trace
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/frida/instrument",data=data,headers=headers)
        return response
    
    def frida_monitor(self):
        data = {
            'hash':self.scan_hash
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/frida/api_monitor",data=data,headers=headers)
        return response
    
    def frida_get_dependencies(self):
        data = {
            'hash':self.scan_hash
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/frida/get_dependencies",data=data,headers=headers)
        return response
    
    def frida_logs(self):
        data = {
            'hash':self.scan_hash
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/frida/logs",data=data,headers=headers)
        return response
    
    def frida_list_script(self):
        data = {
            'device':self.device
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/frida/list_script",data=data,headers=headers)
        return response
    
    def frida_get_script(self,scripts):
        data = {
            'scripts[]':scripts,
            'device':self.device
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f"{self.server}/api/v1/frida/get_script",data=data,headers=headers)
        return response
    
    def Analysis(self):
        self.upload_apk()
        self.scan_apk()
        self.static_json()
        self.get_apps()
        self.start_dynamic_analysis()
        self.dynamic_act_tester("exported")
        self.dynamic_act_tester("test")
        self.dynamic_tls_test()
        self.stop_dynamic_analysis()
        self.dynamic_report_json()
        self.download_pdf()
        self.delete()