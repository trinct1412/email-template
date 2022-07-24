FROM python:3.8.5

#create folder
RUN mkdir ./app/
#set Directory
WORKDIR ./app/

ADD requirements.txt ./app/

ENV PYTHONUNBUFFERED=1
RUN pip3 install -r ./app/requirements.txt

ADD . ./app/

USER root
RUN  chmod +x ./app/
CMD ["python", "send_email.py"]
