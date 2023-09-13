FROM python:3.11.4-slim-buster

WORKDIR /usr/src/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# update and dependencies
RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/project/entrypoint.sh
RUN chmod +x /usr/src/project/entrypoint.sh

# copy project
COPY . .

# setup entrypoint
ENTRYPOINT ["/usr/src/project/entrypoint.sh"]