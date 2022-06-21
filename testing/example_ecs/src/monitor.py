#!/usr/bin/python3
from gRPC.requests import Client
from datetime import datetime
import requests
import os

if __name__=='__main__':
    #placeholder honeypot ID
    hpid = "1234567890"

    #create the client object for connection
    c = Client()

    try: 
        c.send_message(type="status", message=f"alive:{hpid}")
        while True: pass
    finally: c.send_message(type="status", message=f"dead:{hpid}")