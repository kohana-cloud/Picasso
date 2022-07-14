FROM ubuntu:jammy
RUN apt-get update
RUN apt-get -y install python3 python3-pip

#TODO set AWS credentials
#ENV AWS_DEFAULT_REGION=us-east-1

COPY src /opt/
RUN pip3 install -r /opt/requirements.txt
RUN usermod --shell /opt/shell.py root

# Start the orchestrator
WORKDIR /opt/
CMD python3 monitor.py
