#!/usr/bin/python3
from gRPC.requests import Client
from datetime import datetime
import requests
import os
import sys
import time

if __name__=='__main__':
    #placeholder honeypot ID
    hpid = "859a277c-f3ff-11ec-a661-000c2970a8e4"

    #create the client object for connection
    c = Client(tls=False)

    while True:
        time.sleep(1)
        c.send_message(type="status", message=f"alive:{hpid}")


