# Meeseeks, the HipChat bot

## Setup local development environment
1. Install python 3.6 and virtualenv
2. Change to the directory of your local clone of this repository

        cd ~/work/meeseeks
2. Create python virtual environment

        virtualenv -p /usr/bin/python3.6 env
3. Activate python virtual environment

        source env/bin/activate
4. Install required packages

        pip install -r requirements.txt

## Test Message
Send a POST to https://localhost:8070/

    {
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
                "message": "/phones",
                "type": "message"
            },
            "room": {
                "id": 1147567,
                "name": "The Weather Channel"
            }
        },
        "webhook_id": 578829
    }

## Notes
* Authentication is very simple, using ?auth_token= query parameter for
requests. Requests should only transit over public networks using HTTPS.