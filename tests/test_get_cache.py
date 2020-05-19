from datetime import timedelta
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings

from django_cache_framework import GetCache
from tests.service import student_service

settings.configure()


class TestGetCache(TestCase):

    def setUp(self) -> None:
        self.patch_read = patch.object(student_service, 'read', wraps=student_service.read).start()
        self.cached_read = GetCache(key='{args.0}', duration=timedelta(minutes=5))(self.patch_read)

    def test_can_get_cached_result(self):
        student_1 = {'id': uuid4(), 'name': 'student-1'}
        student_2 = {'id': uuid4(), 'name': 'student-2'}
        student_service.create(**student_1)
        student_service.create(**student_2)

        for _ in range(5):
            self.cached_read(student_1['id'])
            self.cached_read(student_2['id'])

        self.assertEqual(2, self.patch_read.call_count)
