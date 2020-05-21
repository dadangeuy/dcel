# Django Cache Expression Language (DCEL)

## Introduction
DCEL is an extension of Django Framework for caching. It provides a more flexible decorator that use an expression language to define the cache key.

## Getting Started

### Cache Method
Use `@Cached` decorator to declare a cached method. This will check the cache before executing the actual method. If the defined key is already cached, it'll immediately return the cached return value. Else, it will execute the actual method, and update the cache using the defined key and return value.
```
class StudentService:
    def __init__(self):
        self.students = []

    @Cached(key='{id}', duration=timedelta(minutes=5))
    def read(self, id: UUID) -> Optional[dict]:
        return first(
            filter(
                lambda s: s['id'] == id, self.students
            ),
            None
        )
```

Use `@CacheUpdate` decorator to declare a cache update method. This will update the cache using the defined key and return value after executing the actual method.
```
class StudentService:
    def __init__(self):
        self.students = []

    @CacheUpdate(key='{id}', duration=timedelta(minutes=5))
    def update(self, id: UUID, name: str) -> dict:
        student = self.read(id)
        student['name'] = name
        return student
```

Use `@CacheInvalidate` decorator to declare a cache invalidate method. This will invalidate cache using the defined key after method executing the actual method.
```
class StudentService:
    def __init__(self):
        self.students = []

    @CacheInvalidate(key='{id}')
    def delete(self, id: UUID) -> dict:
        student = self.read(id)
        self.students.remove(student)
        return student
```

### Cache Key
Cache key is derived from method argument. The syntax is similar to python `f-string`, with some limitation. You can define key using primitive, object, dictionary, list, tuple data type variable. Variable should be enclosed in curly braces (`{}`), and string index should be enclosed in quotation mark (`""` or `''`).
```
class UtilService:

    @staticmethod
    @Cached(key='sum: {a} {b}')
    def sum(a: int, b: int) -> int:
        return a + b
        
    @staticmethod
    @Cached(key='join name: {a["name"]} {b["name"]}')
    def join_name(a: dict, b: dict) -> str:
        return ''.join((a['name'], b['name']))
        
    @staticmethod
    @Cached(key='is lowest: {values[0]} {values[-1]}')
    def is_lowest(values: Union[list, tuple]) -> bool:
        return values[0] <= values[-1]
        
    @staticmethod
    @Cached(key='duration: {started_at.day} {finished_at.day}')
    def duration(started_at: datetime, finished_at: datetime) -> timedelta:
        return finished_at - started_at
```
Nested variable, for example `join_name: {a[b["name"]]}` is not supported.
