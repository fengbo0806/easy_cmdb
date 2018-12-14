#!/usr/bin/env python

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
    # def __init__(self):
    #     super(CallbackBase, self).__init__()
    #     self.consquence = None

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))
        # self.consquence = {host.name: result._result}
        # # consquence = json.dumps({host.name: result._result}, indent=4)
        # return self.consquence


# since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
Options = namedtuple('Options',
                     ['connection', 'hosts','ansible_remote_port', 'module_path', 'forks', 'become', 'become_method',
                      'become_user', 'check', 'diff',
                      'private_key_file'])
options = Options(connection='local', hosts='172.20.51.22,',ansible_remote_port=22, module_path=['/to/mymodules'], forks=10, become=None,
                  become_method=None,
                  become_user='root', check=False, diff=False, private_key_file='~/.ssh/id_rsa')

# initialize needed objects
loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
passwords = dict(vault_pass='cctv.com')

# Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
results_callback = ResultCallback()

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources='localhost,')

# variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)

# create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
play_source = dict(
    name="Ansible Play",
    hosts='172.20.51.22,',
    gather_facts='no',
    tasks=[
        dict(action=dict(module='shell', args='ip add'), register='shell_out', ),
        # dict(action=dict(module='setup', ), register='shell_out'),
        # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)
# print(play_source)
# Create play object, playbook objects use .load instead of init or new methods,
# this will also automatically create the task objects from the info provided in play_source
play = Play().load(play_source, variable_manager=variable_manager, loader=loader, )

# playbook = PlaybookExecutor(
#         playbooks=play_source,
#         inventory=inventory,
#         variable_manager=variable_manager,
#         loader=loader,
#         options=options,
#         passwords=None
#
# )
# res = playbook.run()
# Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks

tqm = None
try:
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=None,
        # stdout_callback=results_callback,
        # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
    )
    # atest = tqm
    # atest.run(play)
    tqm.run(play, )  # most interesting data for a play is actually sent to the callback's methods
    # print(type(tqm._stdout_callback.consquence))
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

'''
changed
end
stdout
cmd
rc
start
stderr
delta
invocation
_ansible_parsed
stdout_lines
stderr_lines
_ansible_no_log'''
