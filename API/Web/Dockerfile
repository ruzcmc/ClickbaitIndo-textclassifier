FROM python:3.8.7

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "gunicorn" ]

CMD [ "--certfile=certificate/server.crt", "--keyfile=certificate/server.key", "-b", "0.0.0.0:5000", "app:app" ]
