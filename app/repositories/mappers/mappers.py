from app.models import UserOrm, TeamOrm, TeamMemberOrm, TaskOrm, EvaluationOrm, MeetingOrm, MeetingParticipantOrm
from app.models.comments import CommentOrm
from app.repositories.mappers.base import DataMapper
from app.schemas.comments import Comment
from app.schemas.evaluations import Evaluation
from app.schemas.meetingparticipants import MeetingParticipant
from app.schemas.meetings import Meeting
from app.schemas.tasks import Task
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

class TaskDataMapper(DataMapper):
    db_model = TaskOrm
    schema = Task

class CommentDataMapper(DataMapper):
    db_model = CommentOrm
    schema = Comment

class EvaluationDataMapper(DataMapper):
    db_model = EvaluationOrm
    schema = Evaluation

class MeetingDataMapper(DataMapper):
    db_model = MeetingOrm
    schema = Meeting

class MeetingParticipantDataMapper(DataMapper):
    db_model = MeetingParticipantOrm
    schema = MeetingParticipant
