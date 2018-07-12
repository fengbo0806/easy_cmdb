from django.shortcuts import render
import winrm
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
rest_pro= s.run_ps('Get-Process | Where-Object {$_.ProcessName.Contains("cloudia") } | Stop-Process -Force')
#start_pro = s.run_ps("Start-Process -FilePath 'C:\Sobey\EMDC\MPC\Cloudia\cloudia.exe' -credential administrator")
#dir_this = s.run_ps('$PSScriptRoot')
#print(dir_this.std_out)
#start_pro.std_err