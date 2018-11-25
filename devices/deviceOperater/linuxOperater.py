import subprocess
'''
ansible  all -i "10.168.101.179," -m ping

ansible-playbook -i "10.168.101.179," test.yml
'''
a = subprocess.Popen(
    'ansible all -i "172.20.51.22," -m setup -a "filter=ansible_os_family" --key-file=\'~/.ssh/id_rsa\' --user=root',
    shell=True, stdout=subprocess.PIPE, )
# a = subprocess.Popen('pwd',shell=True ,stdout=subprocess.PIPE,)
b = a.stdout.read()
print(b)
