from datetime import timedelta
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings

from dcel import ReadCache, DeleteCache
from tests.service import student_service

if not settings.configured:
    settings.configure()


class TestGetCache(TestCase):

    def setUp(self) -> None:
        self.patch_read = patch.object(student_service, 'read', wraps=student_service.read).start()
        self.cached_read = ReadCache(key='{args.0}', duration=timedelta(minutes=5))(self.patch_read)

        self.patch_delete = patch.object(student_service, 'delete', wraps=student_service.delete).start()
        self.cached_delete = DeleteCache(key='{args.0}')(self.patch_delete)

    def test_can_delete_cached_result(self):
        init_student = {'id': uuid4(), 'name': 'student-1'}
        created_student = student_service.create(**init_student)
        self.assertDictEqual(init_student, created_student)

        first_read_student = self.cached_read(created_student['id'])
        self.assertDictEqual(created_student, first_read_student)

        deleted_student = self.cached_delete(created_student['id'])
        self.assertDictEqual(first_read_student, deleted_student)

        second_read_student = self.cached_read(created_student['id'])
        self.assertIsNone(second_read_student)
