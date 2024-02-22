# Author: Suprateem Banerjee [www.github.com/suprateembanerjee]

FROM jupyter/scipy-notebook

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

COPY src ./src
COPY res ./res