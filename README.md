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


For runing the project, just run ``python netatmo.py`` in terminal.
