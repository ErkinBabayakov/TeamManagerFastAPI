from app.exceptions import ObjectNotFoundException, TaskNotFoundException
from app.schemas.comments import CommentRequestAdd, CommentAdd
from app.services.base import BaseService

class CommentService(BaseService):

    async def add_comment(self, task_id: int, author_id: int, comment_data: CommentRequestAdd):
        new_comment_data = CommentAdd(
            task_id=task_id,
            author_id=author_id,
            text=comment_data.text
        )
        try:
            task_exists = await self.db.tasks.check_task_exists(task_id)
            if task_exists:
                await self.db.comments.add(new_comment_data)
                await self.db.commit()
            else:
                raise ObjectNotFoundException
        except ObjectNotFoundException:
            raise TaskNotFoundException

    async def get_comments(self, task_id: int):
        try:
            task_exists = await self.db.tasks.check_task_exists(task_id)
            if task_exists:
                return await self.db.comments.get_all(task_id=task_id)
            else:
                raise ObjectNotFoundException
        except ObjectNotFoundException:
            raise TaskNotFoundException
