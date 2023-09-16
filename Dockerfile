# SET BASE IMAGE OS
FROM python:3.9-slim-bullseye

# UPDATE AND INSTALL GIT
RUN apt update
RUN apt -y install git

# CLONE REPOSITORY
RUN git clone \
    https://github.com/tracemoepy/dragon \
    /home/dragon ; chmod 777 /home/dragon

# SET GIT CONFIG
RUN git config --global user.name "dragon"
RUN git config --global user.email "dragon@e.mail"

# WORKDIR
WORKDIR /home/dragon

# COPY CONFIG IF AVAILABLE
RUN cp config.env ./ || true

# IGNORE PIP WARNING
ENV PIP_ROOT_USER_ACTION=ignore

# UPDATE PIP
RUN pip install -U pip

# INSTALL REQUIREMENTS
RUN pip install -U \
                --no-cache-dir \
                -r requirements.txt

# COMMAND TO RUN
CMD ["python", "main.py"]