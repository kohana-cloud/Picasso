#!/usr/bin/python3
from gRPC.requests import Client
import os

from subprocess import Popen, PIPE
from threading import Thread

def spawn_shell():
    #os.system('bash')
    
    c = Client()

    #p = Popen('/bin/bash', shell=True, executable='/bin/bash')
    #(output, err) = p.communicate()
    
    with Popen('/bin/bash') as p:
        #stdout=PIPE, stdin=PIPE
        #for line in p.stdout:
        #    c.send_message(type="command", message=f"stdout:{line.encode('ascii')}")
            
        """for line in p.stdout:
            for input in p.stdin:
                p.run(input)
            c.send_message(type="command", message=f"stdout:{line}")"""

    
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)




if __name__ == '__main__':
    # start a client (distinct thread) which keeps connection to server open
    c = Client(tls=False)

    hpid = "859a277c-f3ff-11ec-a661-000c2970a8e4"
    src_address = "1.2.3.4"

    c.send_message(type="connection", message=f"connect:{hpid}:{src_address}")


    shell_thread = Thread(target=spawn_shell)
    shell_thread.start()

    # Wait for the shell to terminate
    shell_thread.join()
    

    c.send_message(type="connection", message=f"disconnect:{hpid}:{src_address}")


"""
import os
import fcntl
import subprocess
p = subprocess.Popen(['./test5.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
fd = p.stdout.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
p.stdout.read()

p.stdin.write(b'u')
p.stdin.flush()

p.stdout.read()

p.stdin.write(b'u')
p.stdin.flush()

p.stdout.read()
p.poll()

p.stdin.write(b'q')
p.stdin.flush()

p.poll()"""