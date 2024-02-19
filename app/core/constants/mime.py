from enum import Enum


class MimeTypes(str, Enum):
    JSON = "application/json"
    TEXT = "plain/text"
