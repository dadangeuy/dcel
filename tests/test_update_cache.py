from datetime import timedelta
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings

from django_cache_framework import GetCache, UpdateCache
from tests.service import student_service

settings.configure()


class TestGetCache(TestCase):

    def setUp(self) -> None:
        self.patch_read = patch.object(student_service, 'read', wraps=student_service.read).start()
        self.cached_read = GetCache(key='{args.0}', duration=timedelta(minutes=5))(self.patch_read)

        self.patch_update = patch.object(student_service, 'update', wraps=student_service.update).start()
        self.cached_update = UpdateCache(key='{args.0}', duration=timedelta(minutes=5))(self.patch_update)

    def test_can_update_cached_result(self):
        init_student = {'id': uuid4(), 'name': 'student-1'}
        created_student = student_service.create(**init_student)
        first_read_student = self.cached_read(init_student['id'])
        self.assertEqual(created_student['name'], first_read_student['name'])

        updated_student = self.cached_update(created_student['id'], 'student-2')
        second_read_student = self.cached_read(init_student['id'])
        self.assertEqual(updated_student['name'], second_read_student['name'])
