from fabric import Connection, task
from invoke import Responder


# from fabric.config import
# 2.4.0
# fabric.config.Config

class restart(object):
    def __init__(self, ipadd, port, user, passwd):
        self.ipadd = ipadd
        self.port = port
        self.user = user
        self.passwd = passwd

    def restProcess(self):
        Conn = Connection(
            host=self.ipadd,
            user=self.user,
            port=self.port,
            connect_kwargs={
                # "key_filename": "/home/myuser/.ssh/private.key",
                "password": self.passwd,
            },
        )
        sudopass = Responder(
            pattern=r'\[sudo\] password:',
            response='cctv.com\n',
        )
        # result = Conn.run('uname -s', hide=True)
        # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        # print(result.stdout)
        # print(result)
        # result2 = Conn.run('killall daemon',  pty=True, watchers=[sudopass])
        # result2 = Conn.run('export DISPLAY=:0 ;daemon VSMplayer',  pty=True, watchers=[sudopass])
        with Conn as c:
            result2 = c.run('ps -ef | grep VSMplayer').stdout
            # result3 = Conn.run('su', watchers=[sudopass]).stdout
            print(result2)


if __name__ == '__main__':
    res = restart()
    res.restProcess()
'''
NoValidConnectionsError(errors)
paramiko.ssh_exception.NoValidConnectionsError: [Errno None] Unable to connect to port 22 on 172.20.215.11
'''

'''
Command exited with status 0.
=== stdout ===
Linux

Ran 'uname -s' on 172.20.51.11, got stdout:
Linux
'''
