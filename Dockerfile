FROM ubuntu:20.04
MAINTAINER Eduardo Gonçalves "https://github.com/eduardofcbg"

RUN yes | unminimize

RUN apt-get update && \
    apt-get install -y openssh-server tree vim nano htop tar man sudo adduser less

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
