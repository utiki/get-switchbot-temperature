FROM python:3.12-slim
USER root

RUN apt-get update && \
    apt-get install -y locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
    
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TZ=Asia/Tokyo

COPY ./requirements.txt ./

RUN pip install --no-warn-script-location --upgrade pip 
RUN pip install --no-warn-script-location -r requirements.txt
CMD ["uvicorn", "main:app", "--workers", "16", "--backlog", "65535", "--host", "0.0.0.0", "--port", "8000"]
