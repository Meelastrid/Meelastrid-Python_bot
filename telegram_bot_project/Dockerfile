FROM python:3.10-alpine AS builder

WORKDIR /code

COPY requirements.txt /code
RUN pip3 install -r requirements.txt

COPY . /code

ENTRYPOINT ["python3"]
CMD ["bot.py"]

