FROM python:slim
ADD db_utils.py /
ADD TempHumid.py /
RUN apt-get update \
	&& apt-get install -y gcc \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install Adafruit_CharLCD Adafruit_DHT pysqlite3 rpi.gpio requests
CMD [ "python", "-u", "./TempHumid.py" ]