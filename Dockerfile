FROM debian:12.2

RUN apt update && \
    apt install -yy build-essential python3 python3-pip python3-venv nodejs npm

RUN apt install -y iverilog gtkwave yosys

RUN npm install -g netlistsvg

COPY requirements.txt /tmp/
RUN pip install --break-system-packages -r /tmp/requirements.txt

WORKDIR /workspace
