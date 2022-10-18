import uuid

genres = [{
    'id': str(uuid.uuid4()),
    'name': 'Science Fiction',
    'description': 'Example of genre for tests',
} for _ in range(10)]
