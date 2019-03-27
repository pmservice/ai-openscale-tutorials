FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget bash linux-headers
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && apk --no-cache --update-cache add gcc gfortran build-base freetype-dev libpng-dev openblas-dev \
  && pip install numpy pandas \
  && pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && pip install --upgrade -r /tmp/requirements.txt\
  && apk del build-dependencies

COPY . /app
ENV FLASK_APP=server/__init__.py
CMD ["python", "manage.py", "start", "0.0.0.0:3000"]
