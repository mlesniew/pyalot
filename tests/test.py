import unittest

import mock

from pyalot import pyalot

PUSHALOT_API_URL = 'https://pushalot.com/api/sendmessage'

class PyalotParams(unittest.TestCase):
    TEST_TOKEN = '0' * 32
    BODY = 'Hello, tests!'
    TITLE = 'Notification title'
    SOURCE = 'Notification source'
    LINK = 'https://github.com/mlesniew/pyalot'
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

