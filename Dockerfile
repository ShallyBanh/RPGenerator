FROM ubuntu:18.04
ARG USR=dev
RUN useradd -ms /bin/bash $USR && \
    apt update && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt -y install python3.7 && \ 
    apt install -y python3-pip && \
    python3.7 -m pip install pygame && \
    python3.7 -m pip install pygame-menu
WORKDIR /home/$USR
USER $USR