from __future__ import absolute_import
from __future__ import unicode_literals

import requests

# URL to pushalot.com notification sending endpoint
PUSHALOT_API_URL = 'https://pushalot.com/api/sendmessage'


class PyalotError(Exception):
    pass


def pyalot(body, title=None, source=None,
           link=None, link_title=None, image=None,
           important=False, silent=False, ttl=None,
           token=None,
           url=PUSHALOT_API_URL):

    # construct the data to post
    data = {
        'AuthorizationToken': token,
        'Body': body,
    }

    if title:
        data['Title'] = title
    if source:
        data['Source'] = source
    if link:
        data['Link'] = link
    if link and link_title:
        data['LinkTitle'] = link_title
    if image:
        data['Image'] = image
    if important:
        data['IsImportant'] = 'True'
    if silent:
        data['IsSilent'] = 'True'
    if ttl:
        data['TimeToLive'] = int(ttl)

    # do the REST API request
    try:
        response = requests.post(url, data=data)
    except requests.ConnectionError as e:
        raise PyalotError('Connection failed: %s' % e)
    except requests.exceptions.RequestException as e:
        raise PyalotError('Request failed: %s' % e)

    try:
        respdata = response.json()
    except ValueError:
        raise PyalotError('Malformed JSON response')

    if not isinstance(respdata, dict):
        raise PyalotError('Invalid REST response')

    if not respdata.get('Success'):
        raise PyalotError(respdata.get('Description', 'Unknown API error'))
