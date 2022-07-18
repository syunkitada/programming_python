FROM ubuntu

RUN apt update
RUN apt install -y openssh-server sudo
RUN mkdir /var/run/sshd

EXPOSE 22
ENTRYPOINT [ "/usr/sbin/sshd", "-D" ]
