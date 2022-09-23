import enum


class ElasticIndexes(str, enum.Enum):
    movies = 'movies'
    genres = 'persons'
    persons = 'persons'
