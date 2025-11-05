from dataclasses import dataclass, field
from time import time

@dataclass
class PostRecord:
    userId: int
    id: int
    title: str
    body: str
    last_used: float = field(default_factory=time)

@dataclass
class CommentRecord:
    postId: int
    id: int
    name: str
    email: str
    body: str
    last_used: float = field(default_factory=time)