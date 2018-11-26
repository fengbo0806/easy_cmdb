import winrm
#winrm 0.3.0
import fabric
#fabric 2.4.0
import ansible
#ansible 2.7.1
# Create your views here.
# s = winrm.Session('192.168.209.162', auth=('*', '*'),transport='ntlm')
# s = winrm.Session('https://172.30.200.149:5986/wsman', auth= ('chry', 'p'))
#
#r = s.run_cmd('ipconfig', ['/all'])
#print(r.std_out)
def auto_ss():
    from winrm.protocol import Protocol

    p = Protocol(
        endpoint='http://172.30.200.149:5985/wsman',
        transport='basic',
        username=r'chry',
        password='pr0t0ss',
        server_cert_validation='ignore')
    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
#rest_cp = s.run_ps('Restart-Computer -Force')
#rest_pro= s.run_ps('Get-Process | Where-Object {$_.ProcessName.Contains("cloudia") } | Stop-Process -Force')
#start_pro = s.run_ps("Start-Process -FilePath 'C:\Sobey\EMDC\MPC\Cloudia\cloudia.exe' -credential administrator")
#dir_this = s.run_ps('$PSScriptRoot')
#print(dir_this.std_out)
#start_pro.std_err

from fabric import Connection


class connectToHost():
    def conToLinux(self):
        # host='xuedan@10.78.104.8:60022'
        host = 'root@172.20.51.22:22'
        command = 'reboot'
        # c=Connection(host,gateway=Connection(gatewayhost,connect_kwargs={'key_filename':'/home/chry/.ssh/id_rsa'}))
        c = Connection(host=host, connect_kwargs={'key_filename': '/home/chry/.ssh/id_rsa'})
        result = c.run(command=command)

        c.close()
    def conTOWindows(self):
        pass
    def conTONetwork(self):
        pass
class operates(object):
    def __init__(self,client,device_type,operation,):
        self.client=client
        self.device_type=device_type
        self.operation=operation
    def connectToHost(self):
        con = Connection(host=self.client,connect_kwargs={'key_filename':'/home/chry/.ssh/id_rsa'})
        return con
    def choseOperations(self):
        if self.operation=='getInfo':
            self.getInfo()
        elif self.operation=='reboot':
            self.reboot()
    def getInfo(self):
        return self.connectToHost()
    def getProcessInfo(self):
        pass
    def getFiles(self):
        pass
    def startProcess(self):
        pass
    def rebootProcess(self):
        pass
    def killProcess(self):
        pass
    def reboot(self):
        self.connectToHost().run(command='reboot')
    def shutDown(self):
        pass
#!/usr/bin/env python

import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

# since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
options = Options(connection='local', module_path=['/to/mymodules'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

# initialize needed objects
loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
results_callback = ResultCallback()

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources='localhost,')

# variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)

# create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
play_source =  dict(
        name = "Ansible Play",
        hosts = 'localhost',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='shell', args='ls'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
         ]
    )

# Create play object, playbook objects use .load instead of init or new methods,
# this will also automatically create the task objects from the info provided in play_source
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
          )
    result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
finally:
    # we always need to cleanup child procs and the structres we use to communicate with them
    if tqm is not None:
        tqm.cleanup()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)



if __name__ == '__main__':
    doOperate = operates(client='root@172.20.51.22:22',device_type='linux',operation='reboot')
    doOperate.reboot()
'''
ansible localhost -m shell -a "ps -ef |  awk '/task/{ print \$2,\$3,\$8 }'" --key-file='~/.ssh/id_rsa' --user=root

ps -aux


'''