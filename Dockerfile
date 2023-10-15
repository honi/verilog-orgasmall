FROM debian:12.2

RUN apt update && \
    apt install -yy build-essential python3 python3-pip python3-venv

RUN apt install -y iverilog gtkwave

COPY requirements.txt /tmp/
RUN pip install --break-system-packages -r /tmp/requirements.txt

WORKDIR /workspace
