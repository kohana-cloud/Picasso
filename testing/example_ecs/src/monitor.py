#!/usr/bin/python3
from gRPC.requests import Client
from datetime import datetime
from threading import Thread
import requests
import os
import time
import psutil


hpid = "859a277c-f3ff-11ec-a661-000c2970a8e4"
pulse_interval_seconds = 1
usage_interval_seconds = 5


def pulse():
    c = Client(tls=False)

    while True:
        c.send_message(type="status", message=f"heartbeat:{hpid}")
        time.sleep(pulse_interval_seconds)

def usage():
    c = Client(tls=False)

    while True:
        print('CPU usage is: ', psutil.cpu_percent(usage_interval_seconds))
        print('Memory usage is:', psutil.virtual_memory()[2])


        p = psutil.Process()
        io_counters = p.io_counters()
        disk_usage_process = io_counters[2] + io_counters[3] # read_bytes + write_bytes
        disk_io_counter = psutil.disk_io_counters()
        disk_total = disk_io_counter[2] + disk_io_counter[3] # read_bytes + write_bytes

        print(disk_io_counter)
        print(disk_total)
        print(disk_usage_process/disk_total * 100)
        
        ##c.send_message(type="status", message=f"heartbeat:{hpid}")
        #n_c = tuple(psutil.disk_io_counters())

        #print(n_c)
        #n_c = []
        """n_c = [(100.0*n_c[i+1]) / n_c[i] for i in xrange(0, len(n_c), 2)]
        print n_c"""

        print()
        
    


if __name__ == '__main__':
    # start a client (distinct thread) which keeps connection to server open
    
    pulse_thread = Thread(target=pulse)
    pulse_thread.start()

    usage_thread = Thread(target=usage)
    usage_thread.start()

    # Wait for the pulse to terminate
    pulse_thread.join()