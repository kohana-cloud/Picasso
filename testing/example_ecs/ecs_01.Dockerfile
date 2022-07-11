FROM ubuntu:20.04
COPY src /src

WORKDIR /src

RUN apt-get update
RUN apt-get upgrade -y

# weird tzdata bug
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get install -y python3 python3-pip ssh
RUN pip3 install -r /src/requirements.txt

RUN echo "root:root" | chpasswd
RUN usermod --shell /src/shell.py root
RUN service ssh start

CMD python3 /src/monitor.py
#CMD ["/usr/sbin/sshd","-D"]