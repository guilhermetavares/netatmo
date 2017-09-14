Netatmo
--------

Using Python implement a single file program that retrieves from Netatmo cloud an access token that allows to access the list of devices of a given user.
The program MUST include the following steps:

a. Receive the user authorization request via HTTP
b. Redirect the user to the Netatmo authorization/authentication endpoint
c. Receive the token exchange code
d. Exchange the token code for a valid token using Netatmo cloud
e. Retrieve and output the user devices list


Solution
--------

For use this app, you need create a app in ``https://dev.netatmo.com/myaccount/``

Firt, you nedd to install the ``requirements.txt``:
    
    Flask==0.12.2
    requests==2.18.3


Also, you nedd to set the vairables in the enviroment:
	
	export SECRET_KEY='111' # for you only safety, but its optional - default '123'
	export NETATMO_APP_ID='52r7622' # your API netatmo client ID
	export NETATMO_CLIENT_SECRET='26t82gi2ug2' # yout API netatmo secret
	export PORT='8000' # default 8000, but its optional


For runing the project, just execute ``python netatmo.py`` in terminal.

This project has deployed in Heroku:
  
    http://netatmo-devices.herokuapp.com/


Step by Step
------------

Considering, the url of project ``<PROJECT_URL>``.


a. The url ``<PROJECT_URL>/login`` receive a user authorization request


b. In the ``login``, the Netatmo authorization/authentication endpoint has is configured for the class ``NetatmoClient`` and the user is redirected:


c. After the user authenticate in ``NetAtmo`` auth page, user is redirected to page ``<PROJECT_URL>/authenticate`` with a ``code`` in the ``GET`` params.


d. With this ``code``, the ``access_token`` is acquired by api ``https://api.netatmo.com/oauth2/token`` using ``NetatmoClient`` and saved in the session. if the process of acquiring the ``access_token`` was successful, the user is redirected for the ``<PROJECT_URL>/devices``


e. In the ``<PROJECT_URL>/devices``, if exists a ``access_token`` in ``session`` the page returns the devices list per api ``https://api.netatmo.com/api/partnerdevices``. If the token is expired a new token is generate in the ``<PROJECT_URL>/refresh``

     