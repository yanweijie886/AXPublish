import json
import platform
config_json='./config/config.json'
with open(config_json) as f:
    PATH = json.load(f)['path']


#print(platform.system())

if platform.system() == 'Windows':
    print('Windows系统')
    HOME = 'HOMEPATH'
elif platform.system() == 'Linux':
    print('Linux系统')
    HOME = 'HOME'
else:
    print('其他')
    HOME = 'HOME'