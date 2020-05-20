from datetime import timedelta
from unittest import TestCase

from django.conf import settings

from dcel import ReadCache

if not settings.configured:
    settings.configure()


class TestCreateKey(TestCase):

    def test_can_create_key_from_primitive(self):
        cached_key = None

        def set_cached_key(key: str, _):
            nonlocal cached_key
            cached_key = key

        cached_method = ReadCache(
            key='sum({a},{b})',
            duration=timedelta(minutes=5),
            on_miss=set_cached_key,
        )(self.sum)

        cached_method(1, 2)
        self.assertEqual(cached_key, 'sum(1,2)')

    @staticmethod
    def sum(a: int, b: int) -> int:
        return a + b
