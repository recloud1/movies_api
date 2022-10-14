import enum


class RequestMethods(str, enum.Enum):
    get = 'GET'


class ApiRoutes(str, enum.Enum):
    docs = 'docs'
    films = 'films'
    genres = 'genres'
    persons = 'persons'
