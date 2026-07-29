from app.models.comments import CommentOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import CommentDataMapper


class CommentRepository(BaseRepository):
    model = CommentOrm
    mapper = CommentDataMapper