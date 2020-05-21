from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings

from dcel import Cached
from tests.service import student_service

if not settings.configured:
    settings.configure()


class TestCached(TestCase):

    def setUp(self) -> None:
        self.patch_read = patch.object(student_service, 'read', wraps=student_service.read).start()
        self.cached_read = Cached(key='{args[0]}')(self.patch_read)

    def test_can_read_cached_result(self):
        init_student_1 = {'id': uuid4(), 'name': 'student-1'}
        created_student_1 = student_service.create(**init_student_1)
        self.assertDictEqual(init_student_1, created_student_1)

        init_student_2 = {'id': uuid4(), 'name': 'student-2'}
        created_student_2 = student_service.create(**init_student_2)
        self.assertDictEqual(init_student_2, created_student_2)

        for _ in range(5):
            read_student_1 = self.cached_read(created_student_1['id'])
            read_student_2 = self.cached_read(created_student_2['id'])
            self.assertDictEqual(created_student_1, read_student_1)
            self.assertDictEqual(created_student_2, read_student_2)

        self.assertEqual(2, self.patch_read.call_count)
