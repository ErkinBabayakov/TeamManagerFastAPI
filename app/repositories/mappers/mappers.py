from app.models import UserOrm, TeamOrm, TeamMemberOrm
from app.repositories.mappers.base import DataMapper
from app.schemas.teammembers import TeamMember
from app.schemas.teams import Team
from app.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User

class TeamDataMapper(DataMapper):
    db_model = TeamOrm
    schema = Team

class TeamMemberDataMapper(DataMapper):
    db_model = TeamMemberOrm
    schema = TeamMember