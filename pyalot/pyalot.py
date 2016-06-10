import requests

# URL to pushalot.com notification sending endpoint
PUSHALOT_API_URL = 'https://pushalot.com/api/sendmessage'


def pyalot(body, title=None, source=None,
        link=None, link_title=None, image=None,
        important=False, silent=False, ttl=None,
        token=None,
        url=PUSHALOT_API_URL):

    # run a basic parameter check
    if not token:
        raise ValueError('No Pushalot token specified')

    if not body:
        raise ValueError('Notification body empty')

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
    response = requests.post(url, data=data)

    # raise a requests exception if response code is not 2xx
    response.raise_for_status()

