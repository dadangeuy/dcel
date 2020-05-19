from typing import Optional
from uuid import UUID

from more_itertools import first


class StudentService:
    def __init__(self):
        self.students = []

    def create(self, id: UUID, name: str) -> dict:
        student = {
            'id': id,
            'name': name
        }
        self.students.append(student)
        return student

    def read(self, id: UUID) -> Optional[dict]:
        return first(
            filter(
                lambda s: s['id'] == id, self.students
            ),
            None
        )

    def update(self, id: UUID, name: str) -> dict:
        student = self.read(id)
        student['name'] = name
        return student

    def delete(self, id: UUID) -> dict:
        student = self.read(id)
        self.students.remove(student)
        return student


student_service = StudentService()
