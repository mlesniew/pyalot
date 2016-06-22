import unittest

import mock
import requests

from pyalot import pyalot, PyalotError

PUSHALOT_API_URL = 'https://pushalot.com/api/sendmessage'


class PyalotParams(unittest.TestCase):
    TEST_TOKEN = '0' * 32
    BODY = 'Hello, tests!'
    TITLE = 'Notification title'
    SOURCE = 'Notification source'
    LINK = 'https://github.com/mlesniew/pyalot'
    IMAGE = LINK + '.png'
    LINK_TITLE = 'Pyalot on Github'

    ARGS = {
        'body': BODY,
        'token': TEST_TOKEN,
    }
    JSON = {
        'Body': BODY,
        'AuthorizationToken': TEST_TOKEN,
    }

    @mock.patch('requests.post')
    def _run_test(self, args, json, post):
        resp = mock.Mock(requests.Response)
        resp.json = mock.Mock(return_value={'Success': True})
        post.return_value = resp
        pyalot(**args)
        post.assert_called_with(
            PUSHALOT_API_URL,
            data=json)

    def test_basic(self):
        self._run_test(self.ARGS, self.JSON)

    def test_title(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(title=self.TITLE)
        json.update(Title=self.TITLE)
        self._run_test(args, json)

    def test_source(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(source=self.SOURCE)
        json.update(Source=self.SOURCE)
        self._run_test(args, json)

    def test_link(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(link=self.LINK)
        json.update(Link=self.LINK)
        self._run_test(args, json)

    def test_link_title(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(link=self.LINK, link_title=self.LINK_TITLE)
        json.update(Link=self.LINK, LinkTitle=self.LINK_TITLE)
        self._run_test(args, json)

    def test_link_title_only(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(link_title=self.LINK_TITLE)
        self._run_test(args, json)

    def test_image(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(image=self.IMAGE)
        json.update(Image=self.IMAGE)
        self._run_test(args, json)

    def test_important(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(important=True)
        json.update(IsImportant='True')
        self._run_test(args, json)

    def test_not_important(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(important=False)
        self._run_test(args, json)

    def test_silent(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(silent=True)
        json.update(IsSilent='True')
        self._run_test(args, json)

    def test_not_silent(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(silent=False)
        self._run_test(args, json)

    def test_ttl(self):
        args, json = dict(self.ARGS), dict(self.JSON)
        args.update(ttl=321)
        json.update(TimeToLive=321)
        self._run_test(args, json)


class PyalotErors(unittest.TestCase):
    TEST_TOKEN = '0' * 32
    BODY = 'Hello, tests!'

    ARGS = {
        'body': BODY,
        'token': TEST_TOKEN,
    }
    JSON = {
        'Body': BODY,
        'AuthorizationToken': TEST_TOKEN,
    }

    @mock.patch('requests.post',
                side_effect=requests.exceptions.RequestException)
    def _run_test(self, args, json, post):
        post.assert_called_with(
            PUSHALOT_API_URL,
            data=json)

    @mock.patch('requests.post',
                side_effect=requests.exceptions.RequestException)
    def test_request_error(self, post):
        self.assertRaises(PyalotError, pyalot, **self.ARGS)
        post.assert_called_with(PUSHALOT_API_URL, data=self.JSON)

    @mock.patch('requests.post', side_effect=requests.ConnectionError)
    def test_connection_error(self, post):
        self.assertRaises(PyalotError, pyalot, **self.ARGS)
        post.assert_called_with(PUSHALOT_API_URL, data=self.JSON)

    @mock.patch('requests.post')
    def _test_response(self, json_fn, post):
        resp = mock.Mock(requests.Response)
        resp.json = json_fn
        post.return_value = resp
        self.assertRaises(PyalotError, pyalot, **self.ARGS)
        post.assert_called_with(PUSHALOT_API_URL, data=self.JSON)

    @mock.patch('requests.post')
    def test_empty_response(self, post):
        self._test_response(mock.Mock(return_value=''))

    @mock.patch('requests.post')
    def test_empty_response_json(self, post):
        self._test_response(mock.Mock(return_value={}))

    @mock.patch('requests.post')
    def test_failure_response(self, post):
        self._test_response(mock.Mock(return_value={'Success': False}))

    @mock.patch('requests.post')
    def test_malformed_json(self, post):
        self._test_response(mock.Mock(side_effect=ValueError))
