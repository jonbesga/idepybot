# Telegram bot skeleton ready for Heroku deployment

Change the name of settings_sample.ini in the app folder to settings.ini

Replace YOUR_TOKEN_HERE with your bot token.

Add the heroku remote

`heroku git:remote -a <YOUR_HEROKU_APP>`

Push the skeleton to the heroku dyno

`git push heroku master`
