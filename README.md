# IdePy, Telegram bot skeleton ready for Heroku deployment

The following repository contains the code of @IdePyBot a telegram bot. I'm using the following tools:

1. Python 3.
2. Flask, web server to manage the webhooks.
3. Requests library to manage the HTTP requests to the Telegram API.
4. Heroku, for app deployment.

## Installation

Create a Heroku app.

Clone the repository:

```
git clone https://github.com/jabesga/idepybot
cd idepybot
```

Add the heroku remote:

`heroku git:remote -a <YOUR_HEROKU_APP>`

Make the modifications you wish into the code.

Push the code to the heroku dyno

`git push heroku master`

In your Heroku app control panel add the following config vars:

**token** and **app_url**
