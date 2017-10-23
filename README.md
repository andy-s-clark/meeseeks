# Meeseeks, the HipChat bot

## Setup local development environment
1. Install python 3.6 and virtualenv
2. Change to the directory of your local clone of this repository

        cd ~/work/meeseeks
2. Create python virtual environment

        python3.6 -m venv env
3. Activate python virtual environment

        source env/bin/activate
4. Install required packages

        pip install -r requirements.txt

## Configuration
Sensitive data should not be committed to the git repo. Instead it should be
passed in as environment variables or read from files created by
configuration management.

### Environment variables
* `MEESEEKS_AUTH_TOKEN` - When set, requires that a matching `auth_token`
string is sent as a query parameter for every request. Such requests should only
transit over public networks using HTTPS.

### phones.yaml
Dictionary of names and phone numbers
ex.

    'Andy Clark': 530-555-0098
    'Joe Schmo': 530-555-0032
    'John Schmo': 530-555-0075

## Test Message
Send a POST to https://localhost:8070/webhook/

    curl -X POST \
    http://localhost:8070/webhook/ \
    -H 'cache-control: no-cache' \
    -H 'content-type: application/json' \
    -d '{
        "event": "room_message",
        "item": {
            "message": {
                "date": "2015-01-20T22:45:06.662545+00:00",
                "from": {
                    "id": 1661743,
                    "mention_name": "Blinky",
                    "name": "Blinky the Three Eyed Fish"
                },
                "id": "00a3eb7f-fac5-496a-8d64-a9050c712ca1",
                "mentions": [],
                "message": "/help",
                "type": "message"
            },
            "room": {
                "id": 1147567,
                "name": "The Weather Channel"
            }
        },
        "webhook_id": 578829
    }'
