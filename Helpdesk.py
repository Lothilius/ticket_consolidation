__author__ = 'Lothilius'

import requests
import json
import sys
import authentication as auth
from Status import Status
import datetime
import pandas as pd
import re


pd.set_option('display.width', 160)


class Helpdesk(object):
    """ Extend Status class for Helpdesk.
    """
    def __init__(self):
        self.tickets = self.get_all_tickets()

    def get_status(self):
        # One possibility in to poll their twitter account or check load time for loading a HD page.
        if True:
            return 1

    def count_unassigned(self, helpdesk_tickets):
        """Count total unassigned"""
        unassigned_total = 0
        for each in helpdesk_tickets:
            if each['TECHNICIAN'] == '':
                unassigned_total += 1

        return unassigned_total


    def aggregate_tickets(self, ticket_list_a, ticket_list_b):
        """ Join to lists of helpdesk tickets.

        :param ticket_list_a: list
        :param ticket_list_b: list
        :return: list - helpdesk_tickets
        """
        helpdesk_tickets = ticket_list_a + ticket_list_b

        return helpdesk_tickets

    def create_api_request(self, helpdesk_que='Business Applications - Triage_QUEUE', from_value=1):
        """ Create the api request for HD. At the moment very minimal
            but can be expanded in the future for creating more specific and different types of requests.
        :param helpdesk_que: This is the view name that can be created in the requests page
        :param from_value: Sets the beginning value in the list returned
        :return: string of the URL, dict of the query, and a dict of the header
        """
        # Main HDT api URL
        url = "http://sdpondemand.manageengine.com/api/json/request"

        # Query values go in this json structure
        querystring = {"scope":"sdpodapi",
                       "authtoken":auth.hdt_token(),
                       "OPERATION_NAME":"GET_REQUESTS",
                       "INPUT_DATA":"{operation:{"
                                    "Details:{"
                                    "FILTERBY:'%s', FROM:%s, LIMIT:100}}}" % (helpdesk_que, from_value) }

        # Header information
        headers = {
            'cache-control': "no-cache",
            }
        return url, querystring, headers


    def get_100_tickets(self, helpdesk_que='7256000001457777_MyView_7256000001457775', from_value=1):
        """ Get helpdesk tickets for the respective que 100 at a time.
        :return: list of dicts - helpdesk_tickets
        """
        url, querystring, headers = self.create_api_request(helpdesk_que, from_value)

        # Create the request and capture the response.
        response = requests.request("POST", url, headers=headers, params=querystring)

        # Load the response to the request as a json object.
        helpdesk_tickets = json.loads(response.text)

        return helpdesk_tickets["operation"]["Details"]

        # print(json.dumps(helpdesk_tickets["operation"]["Details"], indent=4))

    def get_all_tickets(self):
        try:
            from_value = 1
            # Get first 100 ticket from helpdesk
            helpdesk_tickets = self.get_100_tickets()

            # Check if more than 100 exist and need to be aggregated.
            if len(helpdesk_tickets) == 100:
                # TODO - Make this a recursive method!!!
                while len(helpdesk_tickets) % 100 == 0:
                    from_value = from_value + 100
                    helpdesk_tickets = self.aggregate_tickets(
                        helpdesk_tickets, self.get_100_tickets(from_value=from_value))

            return helpdesk_tickets
        except:
            error_result = "Unexpected error 1: %s, %s" % (sys.exc_info()[0], sys.exc_info()[1])
            # TODO -Fix this issue so that error_message is populated!

            print error_result


def convert_time(unicode_series):
    """Given value for date time
        Convert it to a regular datetime string"""
    # for each in unicode_series:
    if len(unicode_series) == 10:
        pass
    elif len(unicode_series) == 13:
        unicode_series = unicode_series[:10]
    try:
        date_time_value = datetime.datetime.fromtimestamp(int(unicode_series)).strftime('%Y-%m-%d %H:%M:%S')
        if int(date_time_value[:4]) > 2009:
            return date_time_value
        else:
            return unicode_series
    except:
        return unicode_series

def reduce_to_year(unicode_series):
    pattern = re.compile("(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})$")
    match = pattern.match(unicode_series)
    if match:
        return unicode_series[:10]
    else:
        return unicode_series

if __name__ == '__main__':
    status = Helpdesk()
    tickets = pd.DataFrame(status.tickets)
    print tickets
    # tickets = tickets.applymap(convert_time)
    # tickets = tickets.applymap(reduce_to_year)
    # tickets = tickets.groupby(['CREATEDTIME', 'TECHNICIAN'], as_index=False)
    # grouped_tickets = pd.DataFrame(tickets.size(), columns=['Counts'])
    # print grouped_tickets.reset_index()
    # print grouped_tickets
    # print grouped_tickets
    # print grouped_tickets['TECHNICIAN'].transform('count')
