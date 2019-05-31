import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
# from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

consquence = None


class ResultCallback(CallbackBase, ):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    #
    def __init__(self):
        super(CallbackBase, self).__init__()
        self.consquence = None

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))
        self.consquence = {host.name: result._result}
        # # consquence = json.dumps({host.name: result._result}, indent=4)
        return self.consquence


class vsm(object):
    def __init__(self, hosts):
        self.hosts = hosts

    def execude(self):
        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method',
                              'become_user', 'check', 'diff', 'private_key_file',
                              ])
        options = Options(connection='smart', module_path=['/to/mymodules'], forks=10, become=None,
                          become_method=None,
                          become_user='root', check=False, diff=False, private_key_file='~/.ssh/id_rsa', )

        # initialize needed objects
        loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
        passwords = dict(vault_pass='cctv.com')

        # Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
        results_callback = ResultCallback()

        # create inventory, use path to host config file as source or hosts in a comma separated string
        inventory = InventoryManager(loader=loader, sources='/etc/ansible/hosts')
        # inventory.add_host(host='172.20.51.22',port=22,group='test')

        # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
        play_source = dict(
            name="Ansible Play",
            hosts=self.hosts,
            gather_facts='no',
            tasks=[
                dict(action=dict(module='shell', args='ps -ef | grep VSM'), register='shell_out', ),
                # dict(action=dict(module='setup', ), register='shell_out'),
                # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
            ]
        )

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader, )
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=None,
                stdout_callback=results_callback,
                # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            )
            # atest = tqm
            # atest.run(play)
            rs = tqm.run(play, )  # most interesting data for a play is actually sent to the callback's methods
            print('---')
            print()
            # if tqm._stdout_callback.consquence:
            #     for key in tqm._stdout_callback.consquence['172.20.51.22']['stderr']:
            #         print(key,)
        except BaseException:
            print(str(BaseException))
        finally:
            # we always need to cleanup child procs and the structures we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)


if __name__ == '__main__':
    pass

#import json
#import subprocess

# temfile = subprocess.run("ansible-playbook VSMplayer.yml ", shell=True,
#                          # stdout=subprocess.PIPE
#                          )
# print('----')
# print(temfile.stdout)
# json_data = json.loads(temfile.stdout)
# for line in json_data['plays'][0]['tasks'][1]['hosts']['ansible_connection=ssh']['stdout_lines']:
#     print(line)

'''
/etc/ansible/hosts 
'''
#
# restartResult = subprocess.run("ansible-playbook VSMplayerRestart.yml ", shell=True, )
#
# with open('/etc/ansible/hosts ') as ansibleHost:
#     checkpoint = 0
#     for line in ansibleHost:
#         if not line:
#             break
#         if 'vms' in line:
#             checkpoint = 1
#         if checkpoint == 1:
#             '''172.20.51.23 ansible_connection=ssh ansible_host=172.20.51.23 ansible_ssh_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa
# '''
#
#
# class vsm(object):
#     def __init__(self):
#         pass
#
#     def check(self):
#         checkResult = subprocess.run("ansible-playbook VSMplayerCheck.yml ", shell=True, )
#         return checkResult
# !/usr/bin/env python
