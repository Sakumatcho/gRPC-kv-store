FROM python:3.12.4-slim

WORKDIR /work

COPY ./requirements.txt ./requirements.txt

COPY ./.jupyter/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

RUN apt-get update

RUN apt-get install -y htop vim gcc python3-dev git curl isort g++ graphviz sudo

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
