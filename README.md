# Telegram bot skeleton ready for Heroku deployment

Add the heroku remote

`heroku git:remote -a <YOUR_HEROKU_APP>`

Push the skeleton to the heroku dyno

`git push heroku master`

In your Heroku app control panel add the following config vars:

'token' and 'app_url'