FROM python:3.11.3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER root

# install system dependencies
RUN apt-get update
RUN apt-get -y install libnss3-dev libgconf-2-4 libxi6 libxrender1 xvfb libxrandr2 unzip \
               libxss1 libxtst6 libgtk-3-0 libasound2 xdg-utils libu2f-udev libgbm1 fonts-liberation
RUN rm -rf /var/lib/apt/lists/*s

# install chrome browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

# install chrome driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY app /app
COPY .env.prod /.env

WORKDIR /app

CMD ["bash", "./schedule.sh"]
