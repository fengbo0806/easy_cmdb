import json
import subprocess

temfile = subprocess.run("ansible-playbook VSMplayer.yml ", shell=True,
                         # stdout=subprocess.PIPE
                         )
print('----')
print(temfile.stdout)
# json_data = json.loads(temfile.stdout)
# for line in json_data['plays'][0]['tasks'][1]['hosts']['ansible_connection=ssh']['stdout_lines']:
#     print(line)

'''
/etc/ansible/hosts 
'''

checkResult = subprocess.run("ansible-playbook VSMplayerCheck.yml ", shell=True, )
restartResult = subprocess.run("ansible-playbook VSMplayerRestart.yml ", shell=True, )

with open('/etc/ansible/hosts ') as ansibleHost:
    checkpoint = 0
    for line in ansibleHost:
        if not line:
            break
        if 'vms' in line:
            checkpoint = 1
        if checkpoint == 1:

            '''172.20.51.23 ansible_connection=ssh ansible_host=172.20.51.23 ansible_ssh_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa
'''
