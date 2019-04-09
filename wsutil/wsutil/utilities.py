'''
    Utitlity and wrapper functions
'''

#Datetime
from datetime import datetime
from datetime import timedelta

def get_datetime_str(date_time,date_format_out):
    """
        wrapper for datetime.strpfrtime
    """
    return(datetime.strftime(date_time, date_format_out))


def get_datetime(observation_unparsed,date_format_in):
    """
        wrapper for datetime.strptime
    """
    return(datetime.strptime(observation_unparsed, date_format_in))

#Email
import smtplib
import ssl
from email.message import EmailMessage

def send_email(sender, password, receivers, subject, content):
    """
        Send an email through gmail. Intended to alert admin when weather station stalls. 
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    msg.set_content(content)

    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)

        server.send_message(msg)

#BS4
from bs4 import BeautifulSoup

def get_soup(url,tag_names):
    soup = BeautifulSoup(simple_get(url), 'xml')
    tag_objects = list(map(lambda tag: soup.find(tag), tag_names))
    return(tag_objects)

#XML
from xml.etree import ElementTree as ET

def get_tree(url):
    """
        Return an ElementTree representing the XML content
            input: URL of xml content
    """
    xml_raw = simple_get(url)
    root = ET.fromstring(xml_raw)
    tree = ET.ElementTree(root)
    return(tree)

def parse_xml_tag(tree,tag):
    """
        Return content of a unique tag from ElementTree object
    """
    return tree.getroot().find(tag).text

#Web Requests General
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def simple_get(url,headers=None):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of JSON/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True,headers=headers)) as resp:
            if is_good_response(resp):
                if(is_xml(resp)):
                    return resp.content
                elif(is_json(resp)):
                    return resp.json()
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be xml, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and (is_xml(resp) or is_json(resp)))


def is_xml(resp):
    """Return bool for whether resp is xml content"""
    return resp.headers['Content-Type'].lower().find('xml') > -1


def is_json(resp):
    """Return bool for whether resp is json content"""
    return resp.headers['Content-Type'].lower().find('json') > -1


def log_error(e):
    """
    Print Error
    """
    print(e)
    # TODO: Log Errors