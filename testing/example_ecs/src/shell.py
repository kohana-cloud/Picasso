#!/usr/bin/python3
from gRPC.requests import Client
import os

if __name__ == '__main__':
    # start a client (distinct thread) which keeps connection to server open
    c = Client(tls=False)

    hpid = "1234567890"
    src_address = "1.2.3.4"

    c.send_message(type="connection", message=f"connect:{hpid}:{src_address}")

    os.system('/bin/sh')

    c.send_message(type="connection", message=f"disconnect:{hpid}:{src_address}")