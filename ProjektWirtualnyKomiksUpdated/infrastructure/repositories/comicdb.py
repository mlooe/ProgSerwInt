"""Module containing comic repository implementation"""

from typing import Any, Iterable
from sqlalchemy import select, join
from db import (
    comics_table,
    users_table,
    comic_tags_table,
    tags_table,
    database,
)

