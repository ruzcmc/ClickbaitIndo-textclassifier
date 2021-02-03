## API for Clickbait Classifier

### Overview

API for Clickbait Classifier is a web-app built within Flask framework. This API allows users to classify a headline from Indonesian online news headline either it's a clickbait or not.

### Installation Guide

1. In order to deploy this API, you have to train and save the model using our [training script](../Training%20Script.ipynb).
2. While waiting for the training, open your MySQL database and create a new database. After that, import [cbapi.sql](Database/cbapi.sql) to the selected database. This will record any user inputs for model retraining purpose.
3. After the training done and you have successfully saved the model, put it under "model" folder inside Web folder.
4. Under Web directory, copy or rename [.env.example](Web/.env.example) to .env. Open that file and fill the values for each variables.
5. (If you don't use HTTPS you can skip this step) Under certificate directory inside Web, put SSL certificate and key for your domain. Make sure the name of your certificate and key is server.crt and server.key.

If you wish to deploy with Docker, you can use the [Dockerfile](Web/Dockerfile). It already has everything you need to setup the whole app (except for the database part). In case you're not using HTTPS, edit the [Dockerfile](Web/Dockerfile) and change:
> CMD [ "--certfile=certificate/server.crt", "--keyfile=certificate/server.key", "-b", "0.0.0.0:5000", "app:app" ]

to

> CMD [ "-b", "0.0.0.0:5000", "app:app" ]

After that you can continue to build and run the container as usual. If you want to deploy manually then continue with the remaining steps below.

6. Run `pip install -r requirements.txt` to install all the required packages.
7. After all package installed, you can now start the API. Use this command to start the API:
```
gunicorn app:app
```

That command will start your API in localhost on port 5000 (Flask default port). If you wish to open it for public, use this:
```
gunicorn -b 0.0.0.0:5000 app:app
```

If you want to serve in HTTPS, add certificate and its key in gunicorn parameters. For example:
```
gunicorn --certfile=certificate/server.crt --keyfile=certificate/server.key -b 0.0.0.0:5000 app:app
``` 

To run it on background, add `--daemon` at the end of the command. It'll restart everytime the main process get killed.

### Notes

If you're using Docker, when running the container you must add `--network=host` so the app can communicate with the database outside its current container.
