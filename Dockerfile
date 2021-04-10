FROM ubuntu:20.04
MAINTAINER Eduardo Gonçalves "https://github.com/eduardofcgo"

RUN yes | unminimize

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y pkg-config iputils-ping expect openssh-server tree less vim nano curl zip unzip htop tar man sudo adduser libcairo2-dev

RUN mkdir /datasets && cd /datasets && wget "https://esgago.s3-eu-west-1.amazonaws.com/twitter.zip" && unzip twitter.zip && rm twitter.zip

COPY ./etc/vim/vimrc.local /etc/vim/vimrc.local

RUN mkdir /var/run/sshd /root/.ssh

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

EXPOSE 22

COPY requirements.txt /src/
RUN apt-get install -y python3-pip && \
    pip3 install -r /src/requirements.txt

COPY entrypoint.sh /root
CMD ["/root/entrypoint.sh"]
