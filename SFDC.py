__author__ = 'Lothilius'

import requests
import authentication as auth
import sys
from simple_salesforce import Salesforce
import pandas as pd

pd.set_option('display.width', 160)


class SFDC(object):
    """ Extend Status class for Helpdesk.
    """
    def __init__(self):
        self.cases = self.get_all_tickets()

    def get_status(self):
        # Get SFDC Status from Status page.
        sfdc = requests.get("http://trust.salesforce.com/trust/instances/NA3")
        sfdc_reply = sfdc.content
        status = "This instance is available and fully functional." in sfdc_reply
        if status:
            return 1
        else:
            return 0

    def get_error(self):
        #     TODO - Parse site for the error message.
        pass

    def aggregate_tickets(self, ticket_list_a, ticket_list_b):
        """ Join to lists of helpdesk tickets.

        :param ticket_list_a: list
        :param ticket_list_b: list
        :return: list - helpdesk_tickets
        """
        helpdesk_tickets = ticket_list_a + ticket_list_b

        return helpdesk_tickets

    def build_query(self, type='01250000000Hnex', status='In Progress', sub_status='', technician=''):

        if technician == '':
            pass
        else:
            technician = " And OwnerId = '%s'" % technician

        if sub_status == '':
            pass
        else:
            sub_status = " And Sub_Status__c = '%s'" % sub_status

        query = "SELECT Id, Status, Sub_Status__c, OwnerId.Name, Requirement_Name__c, " \
                "Estimated_Hours_To_Complete__c, Release_Date__c FROM Case " \
                "WHERE RecordTypeId = '%s' " \
                "AND " \
                "Status = '%s'%s%s" % (type, status, sub_status, technician)

        return query

    def get_count(self, result):
        return result['totalSize']

    def get_cases(self, environment='staging',
                  type='01250000000Hnex',
                  status='In Progress',
                  sub_status='In Development',
                  technician=''):
        """ Get helpdesk tickets for the respective que 100 at a time.
        :return: OrderedDict that contains totalsize, done, and records. Records in turn is also given as an
                OrderedDict with the actualrecords data.
        """
        user_name, pw, token = auth.sfdc_login(environment)
        sf = Salesforce(username=user_name, password=pw, security_token=token)
        result = sf.query_all(self.build_query())
        print result

        return result

    def get_all_tickets(self):
        try:
            cases = self.get_cases('prod')

            return cases
        except:
            error_result = "Unexpected error 1: %s, %s" % (sys.exc_info()[0], sys.exc_info()[1])
            return error_result


if __name__ == '__main__':
    status = SFDC()
    print status.cases
    # tickets = pd.DataFrame(status.cases)
    #
    # tickets = tickets.groupby(['CREATEDTIME', 'TECHNICIAN'], as_index=False)
    # grouped_tickets = pd.DataFrame(tickets.size(), columns=['Counts'])
    # print grouped_tickets.reset_index()
    # print tickets
