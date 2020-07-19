FROM jupyterhub/jupyterhub:latest

RUN \
    adduser -q --gecos "" --disabled-password user  && \
    echo user:user | chpasswd

RUN \
    adduser -q --gecos "" --disabled-password admin && \
    echo admin:admin | chpasswd

RUN \
    pip3 install --no-cache-dir notebook

