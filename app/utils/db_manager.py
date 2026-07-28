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
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
