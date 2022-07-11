#!/usr/bin/python3
from gRPC.requests import Client
from datetime import datetime
from threading import Thread
import requests
import os
import time


hpid = "859a277c-f3ff-11ec-a661-000c2970a8e4"
interval_seconds = 1


def pulse():
    c = Client()
    #create the client object for connection
    c = Client(tls=False)

    while True:
        c.send_message(type="status", message=f"heartbeat:{hpid}")
        time.sleep(interval_seconds)


if __name__ == '__main__':
    # start a client (distinct thread) which keeps connection to server open
    
    pulse_thread = Thread(target=pulse)
    pulse_thread.start()

    # Wait for the pulse to terminate
    pulse_thread.join()