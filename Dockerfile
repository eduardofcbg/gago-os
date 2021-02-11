FROM ubuntu:20.04
MAINTAINER Eduardo Gonçalves "https://github.com/eduardofcgo"

RUN yes | unminimize

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y pkg-config iputils-ping libcairo2-dev openssh-server tree vim nano curl zip unzip htop tar man sudo adduser less

COPY ./etc/vim/vimrc.local /etc/vim/vimrc.local

RUN mkdir /var/run/sshd /root/.ssh

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

EXPOSE 22

COPY ./leaderboard/requirements.txt /leaderboard/
RUN apt-get install -y python3-pip && \
    pip3 install -r /leaderboard/requirements.txt

COPY entrypoint.sh /root
CMD ["/root/entrypoint.sh"]
