# Personal website

Mostly neglected, but it gets updated from time to time :)

## secrets.py

You need to create a `secrets.py` file and add `get_recaptcha_secret()` in it.

## Dependencies

The project allows the use of SendGrid as your emailing provider, so make sure you install Python requirements to the 
libs folder by running the following in the terminal: - `pip install -t libs -r requirements.txt` 
or `pip install -t libs -r requirements.txt --upgrade`

## Cloud SDK and running the project

Make sure you have Cloud SDK installed. You can run the project by typing `sh run.sh` in the terminal.

## Localhost issues

Logging in might not work sometimes on localhost due to the datastore lag. The app still works on a server.

## Deployment

- `gcloud init` (always use a new configuration and create a new project - unless you created one on Cloud Console before)
- `gcloud app create --region=europe-west` (this creates a new GAE app within the Google Cloud project)
- `gcloud app deploy app.yaml cron.yaml index.yaml queue.yaml --version production` (this uploads all the necessary yaml files and names the version "main". If there are some yaml files missing, remove them from this command.)
- `gcloud app browse` (this opens up the app URL in your browser)

## CI

You have to create a GCLOUD_SERVICE_KEY on Google Cloud and ass it as environment variable to BitBucket.

1. Go to Cloud Console --> IAM
2. Find a GAE service account (should already exist).
4. Get it's private key in JSON format.
5. Save the JSON file somewhere on your computer.
6. Open a terminal, navigate to the JSON file and base64 encode it using this command `base64 json_to_encode.json`
7. Go to BitBucket repository pipelines environment variables and enter GCLOUD_SERVICE_KEY as variable name and 
base64 encoded key from the terminal as variable value. Check the Secure box and add.
