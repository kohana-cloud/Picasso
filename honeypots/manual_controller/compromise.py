#!/usr/bin/python3
from gRPC.requests import Client
import os

from subprocess import Popen, PIPE
from threading import Thread


hpid = os.environ['HPID']
src_address = "1.2.3.4"

if __name__ == '__main__':
    # start a client (distinct thread) which keeps connection to server open
    c = Client(tls=False)

    c.send_message(type="connection", message=f"connect:{hpid}:{src_address}")
    c.send_message(type="connection", message=f"disconnect:{hpid}:{src_address}")
