import enum


class ElasticIndexes(str, enum.Enum):
    movies = 'movies'
    genres = 'genres'
    persons = 'persons'


class PersonRoles(str, enum.Enum):
    director = 'director'
    actor = 'actor'
    writer = 'writer'
