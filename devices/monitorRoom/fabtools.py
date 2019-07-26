from fabric import Connection

class fabAct():
    def __init__(self, host, port, username, passwd):
        self.host = host
        self.passwd = passwd
        self.port = port
        self.username = username

    def conn(self):

        return Connection(host=self.username + '@' + str(self.host), connect_kwargs={"password": str(self.passwd)})

    def restartProcess(self):
        c = self.conn()
        daemonStatus = c.run('ps -ef | grep VSMplayer', hide=True).stdout.strip()
        # print(daemonStatus)
        if 'daemon' in daemonStatus:
            # print(1)
            c.run('ps -ef | grep VSMplayer | grep -v \'daemon\|grep\' | awk \'{print "kill -9 " $2}\'|sh',hide=True)
        else:
            c.run('export DISPLAY=:0 ; daemon VSMplayer ', hide=True)
        vncStatus = c.run()
        "nohup x0vncserver --passwordfile=/root/.vnc/passwd display=':0.0' &>/dev/null"

    def processStatus(self):
        c = self.conn()
        c.run('ps -ef | grep VSMplayer ', hide=True)

    def rebootDev(self):
        c = self.conn()
        c.run('reboot')

    def shutDownDev(self):
        c = self.conn()
        c.run('shutdown -h now')


if __name__ == '__main__':
    pass
