#!/usr/bin/python3
from gRPC.requests import Client
import os
import sys

from threading import Thread

hpid = sys.argv[1]
src_address = "1.2.3.4"

c = Client(tls=False)

def notify():
    c.send_message(type="connection", message=f"connect:{hpid}:{src_address}")


if __name__ == '__main__':
    notify_thread = Thread(target=notify)
    notify_thread.start()

    print(f'here: {hpid}')

    os.system("/bin/sh")

    notify_thread.join()
    c.send_message(type="connection", message=f"disconnect:{hpid}:{src_address}")
