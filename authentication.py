__author__ = 'Lothilius'

import requests
from os import environ


def okta_authentication():
    url = 'https://bazaarvoice.okta.com/api/v1/events?'
    api_key = environ['OKTA_KEY']
    headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'authorization': "SSWS " + api_key,
    'postman-token': "trs8GxmAQxBT2axefZFA98xig"
    }
    return url, headers

def smtp_login():
    username = '%s@bazaarvoice.com' % environ['USER']
    password = environ['MY_PW']

    return username, password

def hdt_token():
    helpdesk_token = environ['HDT_TOKEN']

    return helpdesk_token

def sfdc_login(environment='staging'):
    if environment == 'prod':
        username = '%s@bazaarvoice.com' % environ['SFDC_BIZAPPS']
        password = environ['SFDC_PW']
        token = environ['SFDC_TOKEN']
    else:
        username = '%s@bazaarvoice.com.staging' % environ['SFDC_BIZAPPS']
        password = environ['SFDC_PW']
        token = environ['SFDC_STAGING_TOKEN']

    return username, password, token
