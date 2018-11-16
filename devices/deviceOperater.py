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

if __name__ == '__main__':
    doOperate = operates(client='root@172.20.51.22:22',device_type='linux',operation='reboot')
    doOperate.reboot()
