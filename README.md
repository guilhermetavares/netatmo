
Problem
-------

Using Python implement a single file program that retrieves from Netatmo cloud an access token that allows to access the list of devices of a given user.
The program MUST include the following steps:
a. Receive the user authorization request via HTTP
b. Redirect the user to the Netatmo authorization/authentication endpoint
c. Receive the token exchange code
d. Exchange the token code for a valid token using Netatmo cloud
e. Retrieve and output the user devices list


Solution
--------

Firt, you nedd to install the ``requirements.txt``: ::
    
    Flask==0.12.2


