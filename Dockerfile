FROM python:3
USER root

RUN apt-get update && \
    apt-get install -y locales && \
    apt-get install -y cron && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
    
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TZ=Asia/Tokyo

COPY requirements.txt ./

RUN pip install --no-warn-script-location --upgrade pip 
RUN pip install --no-warn-script-location -r requirements.txt
RUN mkdir -p logs
CMD ["python", "save_temperature_to_db.py"]
