from datetime import timedelta, datetime
from typing import Union
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
        self.assertEqual('sum(1,2)', cached_key)

    def test_can_create_key_from_dict(self):
        cached_key = None

        def set_cached_key(key: str, _):
            nonlocal cached_key
            cached_key = key

        cached_method = ReadCache(
            key='join_name({a["name"]},{b["name"]})',
            duration=timedelta(minutes=5),
            on_miss=set_cached_key,
        )(self.join_name)

        cached_method(
            {'id': 0, 'name': 'a'},
            {'id': 1, 'name': 'b'}
        )
        self.assertEqual('join_name(a,b)', cached_key)

    def test_can_create_key_from_list_or_tuple(self):
        cached_key = None

        def set_cached_key(key: str, _):
            nonlocal cached_key
            cached_key = key

        cached_method = ReadCache(
            key='is_lowest({values[0]},{values[-1]})',
            duration=timedelta(minutes=5),
            on_miss=set_cached_key,
        )(self.is_lowest)

        cached_method([0, 1, 2, 3])
        self.assertEqual('is_lowest(0,3)', cached_key)

        cached_method((0, 1, 2, 3, 4, 5, 6))
        self.assertEqual('is_lowest(0,6)', cached_key)

    def test_can_create_key_from_object(self):
        cached_key = None

        def set_cached_key(key: str, _):
            nonlocal cached_key
            cached_key = key

        cached_method = ReadCache(
            key='duration({started_at.day},{finished_at.day})',
            duration=timedelta(minutes=5),
            on_miss=set_cached_key,
        )(self.duration)

        cached_method(datetime(2020, 1, 1), datetime(2020, 1, 2))
        self.assertEqual('duration(1,2)', cached_key)

    @staticmethod
    def sum(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def join_name(a: dict, b: dict) -> str:
        return ''.join((a['name'], b['name']))

    @staticmethod
    def is_lowest(values: Union[list, tuple]) -> bool:
        return values[0] <= values[-1]

    @staticmethod
    def duration(started_at: datetime, finished_at: datetime) -> timedelta:
        return finished_at - started_at
