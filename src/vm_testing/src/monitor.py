#!/usr/bin/python3
from gRPC.requests import Client
from datetime import datetime
import requests
import os
import sys

if __name__=='__main__':
    #placeholder honeypot ID
    hpid = "1a463804ea"

    #create the client object for connection
    c = Client(tls=False)

    c.send_message(type="status", message=f"{sys.argv[1]}:{hpid}")
    while True: pass


