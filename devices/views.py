from django.shortcuts import render
import winrm
#winrm 0.3.0
import fabric
#fabric 2.4.0
# Create your views here.
s = winrm.Session('192.168.209.162', auth=('*', '*'),transport='ntlm')
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
# host='10.78.43.10:22022'
host='xuedant@10.78.104.8:22'
# gatewayhost='xuedan@10.78.104.8:60022'
command = 'ls'
# c=Connection(host,gateway=Connection(gatewayhost),connect_kwargs={'key_filename':'/home/chry/.ssh/id_rsa'})
c=Connection(host=host,connect_kwargs={'key_filename':'/home/chry/.ssh/id_rsa'})
result = c.run(command=command)

c.close()

# 'host=host:port'
# with Connection('host') as c:
#     c.run('command')
#     c.put('file')
# env.gateway = '192.168.181.2'                             # 指定堡垒机 ip
# env.hosts = ['192.168.181.111', '192.168.181.112']        # 指定 hosts 远程主机
# env.key_filename = '/path/to/id_rsa'     # 指定你的私钥文件
# env.user = 'username'                    # 指定用户名
#
# def touchfile():                         # 随便创建一个任务，用来测试
#     run('touch /tmp/www.txt')
