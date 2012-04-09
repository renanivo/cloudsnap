CloudSnap [![Build Status](https://secure.travis-ci.org/renanivo/cloudsnap.png)](http://travis-ci.org/renanivo/cloudsnap)
=========

A python 2.7 Google App Engine (GAE) script to create images (AMIs) from all of your Amazon EC2 instances.

Configuration
-------------

### settings.py

Copy settings.example.py to settings.py and fill:

- Your AWS account key (AWS['key'])
- Your AWS account secret (AWS['secret'])
- Your GAE's administrator email (LOGGER['sender'])
- Your email to receive logs (LOGGER['to'])

**Obs**: lacks a configuration wizard.

### app.yaml

Since cloudsnap is already taken (by me) you will need to replace the application name with something else. Remember to [signup for an GAE Account](https://appengine.google.com/) and verify the availability of the application name.


### cron.yaml

The cron.yaml is configured according to my needs. Feel free to change the scheduling and timezone according to yours.

Deploying
----------

Download [GAE python SDK](http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python) and follow [application upload instructions](http://code.google.com/appengine/docs/python/gettingstarted/uploading.html).


Development Environment
-----------------------

To set up the project on your development environment, follow these steps:

- Download the APP Engine SDK
- Move the SDK folder to /usr/local/google_appengine (the google_appengine folder may be anywhere. If you place it elsewhere take a look at Makefile and replace the path to run the unit tests)
- Install virtualenv and virtualenvwrapper:  

    sudo pip install virtualenv  
    sudo pip install virtualenvwrapper  

- Clone the project:  

    git clone https://github.com/renanivo/cloudsnap.git  

- Create a new virtualenv on the project folder:  

    virtualenv --no-site-packages cloudsnap  

- Go to the project folder and execute:  

    add2virtualenv cloudsnap  
    make setup  
