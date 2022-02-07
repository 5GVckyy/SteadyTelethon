# We're using Ubuntu 20.10
FROM vckyouuu/geezproject:buster

RUN git clone -b Geez-Userbot https://github.com/5GVckyy/SteadyUserbot /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/5GVckyy/SteadyUserbot/SteadyUserbot/requirements.txt

CMD ["python3","-m","userbot"]
