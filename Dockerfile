# Using Python Slim-Buster
FROM vckyouuu/geezprojects:buster
#━━━━━ Userbot Telegram ━━━━━
#━━━━━ By Steady-Userbot ━━━━━

RUN git clone -b Geez-UserBot https://github.com/vckyou/Geez-UserBot /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/5GVckyy/SteadyUserbot/Steady-Userbot/requirements.txt

EXPOSE 80 443

CMD ["python3","-m","userbot"]
