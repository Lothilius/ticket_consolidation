__author__ = 'Lothilius'

from Helpdesk import Helpdesk
from SFDC import SFDC
import pandas as pd
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import re

tls.set_credentials_file(username='Lothilius', api_key='')
pd.set_option('display.width', 160)

def convert_time(unicode_series):
    """Given value for date time
        Convert it to a regular datetime string"""
    # for each in unicode_series:
    if len(unicode_series) == 10:
        pass
    elif len(unicode_series) == 13:
        unicode_series = unicode_series[:10]
    try:
        date_time_value = datetime.datetime.fromtimestamp(int(unicode_series)).strftime('%Y-%m-%d')
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

def get_hdt():
    hd = Helpdesk()
    tickets = pd.DataFrame(hd.tickets)
    tickets = tickets.applymap(convert_time)
    tickets = tickets.applymap(reduce_to_year)
    group_by = tickets.groupby(['CREATEDTIME', 'TECHNICIAN'], as_index=False)
    grouped_tickets = pd.DataFrame(group_by.size(), columns=['Counts'])
    grouped_tickets = grouped_tickets.reset_index()

    return grouped_tickets

def get_sfdc_cases():
    hd = SFDC()
    tickets = pd.DataFrame(hd.cases)
    tickets = tickets.applymap(convert_time)
    tickets = tickets.applymap(reduce_to_year)
    group_by = tickets.groupby(['CREATEDTIME', 'TECHNICIAN'], as_index=False)
    grouped_tickets = pd.DataFrame(group_by.size(), columns=['Counts'])
    grouped_tickets = grouped_tickets.reset_index()

    return grouped_tickets

grouped_hdt_tickets = get_hdt()
# grouped_sfdc_tickets = get_sfdc_cases()

grouped_hdt_tickets.head()

trace_1 = go.Bar(x=grouped_hdt_tickets['CREATEDTIME'], y=grouped_hdt_tickets['Counts'], name='HDT')


data = [trace_1]
layout = go.Layout(barmode='stack')
url = py.plot(data, filename='pandas-time-series')
# print url
