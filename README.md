# Gmail-deleter

Getting started
---------------

This script will help you to delete unnecessary emails on gmail. It will provide you options to delete all mails, mails from certain category and mails from certain user . It also has an option to empty trash or delete spam mails or get statistics for size of the mail, or frequency of sent/received mails from/to certain user.


Prerequisites
-------------

 - Python3 
 - The [pip](https://pypi.python.org/pypi/pip) package managment tool for Python3
 - Access to Internet and a web browser
 - A Google account with Gmail account enabled
 - matplotlib for Python3 


Turn on Gmail API
-----------------

Follow the [instructions](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name)

Installation
------------

 - Optional: Create a virtual environment 
 
 - Run: 
   
   `pip3 install --upgrade google-api-python-client`
    

(Check requirements.txt for additional informations about requirments for installation)

Usage
-----

 - Copy json file generated from Gmail API to the repository directory 


Run script with:

`python3 gmail-delete.py`
