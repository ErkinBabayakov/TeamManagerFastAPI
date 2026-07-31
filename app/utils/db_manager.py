from app.repositories.comments import CommentRepository
from app.repositories.evaluations import EvaluationRepository
from app.repositories.meetingparticipants import MeetingParticipantRepository
from app.repositories.meetings import MeetingsRepository
from app.repositories.tasks import TaskRepository
from app.repositories.teammembers import TeamMemberRepository
from app.repositories.teams import TeamRepository
from app.repositories.users import UserRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.teams = TeamRepository(self.session)
        self.team_members = TeamMemberRepository(self.session)
        self.tasks = TaskRepository(self.session)
        self.comments = CommentRepository(self.session)
        self.evaluations = EvaluationRepository(self.session)
        self.meetings = MeetingsRepository(self.session)
        self.meetingparticipants = MeetingParticipantRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()
