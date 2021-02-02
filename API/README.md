## API for Clickbait Classifier

### Overview

API for Clickbait Classifier is a web-app built in Flask framework. This API allows users to predict a headline from Indonesian online news headline either it's a clickbait news or not a clickbait news.

### Installation Guide

1. In order to deploy this API, you have to train and save the model using our [training script](../Training%20Script.ipynb).
2. While waiting the training, open your MySQL database and create a new database. After that, import [cbapi.sql](Database/cbapi.sql) to the selected database. This will record any user inputs and the data can be retrieved later for retraining purpose.
3. After training done and you have successfully saved the model, download and put it under "model" folder inside Web folder. There is no model folder currently so you have to create it.
4. Under Web directory, copy or rename [.env.example](Web/.env.example) to .env. Open that file and fill the values for each variables.

If you wish to deploy with Docker, you can use the [Dockerfile](Web/Dockerfile). It already has everything needed to setup the whole app (except for the database part). If you want to deploy manually then continue with the remaining steps below.

5. Run `pip install -r requirements.txt` to install all the required packages.
6. After all package installed, you can now start the API. Use this command to start the API:
```
gunicorn app:app
```

This command will start your API in localhost only at port 5000 (Flask default port). If you wish to open it for public, use command below:
```
gunicorn -b 0.0.0.0:5000 app:app
```

To run it on background, add `--daemon` at the end of the command. It'll restart everytime the main process get killed.

### Notes

If you're using Docker, when running the container you must add `--network=host` so it can communicate with the database outside the container itself.
