import re

from django.contrib.postgres.search import SearchQuery, SearchConfig
from django.db.models import Value
from django.utils.encoding import force_text


# taken from django-watson: https://github.com/etianen/django-watson/blob/2226de139b6e177bfbe2824b1749478dbcce3318/watson/backends.py#L26
RE_POSTGRES_ESCAPE_CHARS = re.compile(r"[&:(|)!><]", re.UNICODE)
RE_SPACE = re.compile(r"[\s]+", re.UNICODE)


# inspired from django-watson:
# https://github.com/etianen/django-watson/blob/2226de139b6e177bfbe2824b1749478dbcce3318/watson/backends.py#L33
# https://github.com/etianen/django-watson/blob/2226de139b6e177bfbe2824b1749478dbcce3318/watson/backends.py#L186


def escape_query(text, re_escape_chars):
    """
    normalizes the query text to a format that can be consumed
    by the backend database
    """
    text = force_text(text)
    text = re_escape_chars.sub(" ", text)  # Replace harmful characters with space.

    return " & ".join("$${0}$$:*".format(word) for word in text.split())


class PrefixSearchQuery(SearchQuery):
    def __init__(self, value, output_field=None, *, config=None, invert=False):
        value = escape_query(value, RE_POSTGRES_ESCAPE_CHARS)
        super().__init__(
            value, output_field, config=config, invert=invert, search_type="raw"
        )
