FROM python:3.11

WORKDIR /usr/src/app

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYRHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY . /usr/src/app/
RUN pip install -r requirements.txt

RUN chmod 755 entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
