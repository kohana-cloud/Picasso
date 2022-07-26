FROM ubuntu:jammy
RUN apt-get update
RUN apt-get -y install python3 python3-pip

RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386

COPY src /opt/
COPY src/shell.py /bin/bash

RUN ln -sf /opt/shell.py /bin/bash
RUN chmod +x /bin/bash
RUN chmod +x /opt/run.sh
RUN pip3 install -r /opt/requirements.txt

# Start the orchestrator
WORKDIR /opt/
CMD /opt/run.sh