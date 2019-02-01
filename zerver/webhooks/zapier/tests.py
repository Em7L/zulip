# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class ZapierHookTests(WebhookTestCase):
    STREAM_NAME = 'zapier'
    URL_TEMPLATE = "/api/v1/external/zapier?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'zapier'

    def test_zapier_when_subject_and_body_are_correct(self) -> None:
        expected_topic = u"New email from zulip@zulip.com"
        expected_message = u"Your email content is: \nMy Email content."
        self.send_and_test_stream_message('correct_subject_and_body', expected_topic, expected_message)

    def test_zapier_when_topic_and_body_are_correct(self) -> None:
        expected_topic = u"New email from zulip@zulip.com"
        expected_message = u"Your email content is: \nMy Email content."
        self.send_and_test_stream_message('correct_topic_and_body', expected_topic, expected_message)

    def test_zapier_weather_update(self) -> None:
        expected_topic = u"Here is your weather update for the day:"
        expected_message = u"Foggy in the morning.\nMaximum temperature to be 24.\nMinimum temperature to be 12"
        self.send_and_test_stream_message('weather_update', expected_topic, expected_message)

class ZapierZulipAppTests(WebhookTestCase):
    STREAM_NAME = 'zapier'
    URL_TEMPLATE = "/api/v1/external/zapier?api_key={api_key}&stream={stream}"
    FIXTURE_DIR_NAME = 'zapier'

    def test_auth(self) -> None:
        payload = self.get_body('zapier_zulip_app_auth')
        headers = {'HTTP_USER_AGENT': 'ZapierZulipApp'}
        result = self.client_post(self.url, payload,
                                  content_type='application/json',
                                  **headers)
        self.assert_json_success(result)

    def test_stream(self) -> None:
        expected_topic = u"Sample message from Zapier!"
        expected_message = u"Hi! I am a new sample message from Zapier!"
        self.send_and_test_stream_message('zapier_zulip_app_stream',
                                          expected_topic, expected_message,
                                          HTTP_USER_AGENT='ZapierZulipApp')
