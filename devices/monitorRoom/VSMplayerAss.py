import json
import subprocess

temfile = subprocess.run("ansible-playbook VSMplayer.yml ", shell=True, stdout=subprocess.PIPE)
print('----')
# print(temfile.stdout)
json_data = json.loads(temfile.stdout)
for line in json_data['plays'][0]['tasks'][1]['hosts']['ansible_connection=ssh']['stdout_lines']:
    print(line)