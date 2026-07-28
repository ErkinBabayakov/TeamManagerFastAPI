from fastapi import HTTPException

class TeamManagerException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class UserNotEnoughRightsException(TeamManagerException):
    detail = "У вас недостаточно прав для выполнения этой операции"

class UserNotManagerOrAdminException(TeamManagerException):
    detail = "Для выполнения операции необходима роль 'manager' или 'admin'"

class ObjectNotFoundException(TeamManagerException):
    detail = "Объект не найден"

class TeamNotFoundException(ObjectNotFoundException):
    detail = "Команда с указанным team_id не найдена"

class MemberRoleUpdateException(TeamManagerException):
    detail = "Ошибка с базой данных. Не удалось обновить роль"

class TeamNotExistException(ObjectNotFoundException):
    detail = "Пока еще не создана ни одна команда"

class TeamEmptyException(TeamManagerException):
    detail = "В команде еще нет ни одного пользователя"

class TeamOrUserNotFoundException(ObjectNotFoundException):
    detail = "Команда или пользователь не найдены"

class ObjectAlreadyExistsException(TeamManagerException):
    detail = "Объект уже существует"

class UserInviteAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже добавлен в команду ранее"

class IncorrectTokenException(TeamManagerException):
    detail = "Неверный токен"

class UserAlreadyExistsException(TeamManagerException):
    detail = "Пользователь с таким email уже сущесвует"

class TeamAlreadyExistsException(TeamManagerException):
    detail = "Команда с таким id и именем существует"

class EmailNotCorrectException(TeamManagerException):
    detail = "Неправильно введён email. Введите корректный email"

class EmailNotRegisteredException(TeamManagerException):
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordException(TeamManagerException):
    detail = "Неверный пароль"

class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден, указан неверный id"

class TokenExpiredException(TeamManagerException):
    detail = "Вы не предоставили токен доступа, пройдите аутентификацию"

class InvalidInviteCodeException(TeamManagerException):
    detail = "Недействительный код приглашения в команду"

class TeamManagerHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserNotEnoughRightsHTTPException(TeamManagerHTTPException):
    status_code = 403
    detail = "У вас недостаточно прав. В этот эндпоинт могут заходить только администраторы системы"

class UserEmailAlreadyExistsHTTPException(TeamManagerHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"

class EmailNotCorrectHTTPException(TeamManagerHTTPException):
    status_code = 401
    detail = "Неправильно введён email. Введите корректный email"

class EmailNotRegisteredHTTPException(TeamManagerHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordHTTPException(TeamManagerHTTPException):
    status_code = 401
    detail = "Неверный пароль"

class UserNotFoundHTTPException(TeamManagerHTTPException):
    status_code = 404
    detail = "Пользователь не найден, указан неверный id"

class TokenExpiredHTTPException(TeamManagerHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа, пройдите аутентификацию"

class UserNotManagerOrAdminHTTPException(TeamManagerHTTPException):
    status_code = 403
    detail = "Для выполнения операции необходима роль 'manager' или 'admin'"

class InvalidInviteCodeHTTPException(TeamManagerHTTPException):
    status_code = 400
    detail = "Недействительный код приглашения в команду"

class TeamNotFoundHTTPException(TeamManagerHTTPException):
    status_code = 404
    detail = "Команда с указанным team_id не найдена"

class TeamOrUserNotFoundHTTPException(TeamManagerHTTPException):
    status_code = 404
    detail = "Команда или пользователь не найдены"

class UserInviteAlreadyExistsHTTPException(TeamManagerHTTPException):
    status_code = 409
    detail = "Пользователь уже добавлен в команду ранее"

class TeamAlreadyExistsHTTPException(TeamManagerHTTPException):
    status_code = 409
    detail = "Команда с таким именем уже существует"

class TeamEmptyHTTPException(TeamManagerHTTPException):
    status_code = 404
    detail = "Команда с указанным team_id не существует, или в команде еще нет ни одного пользователя"

class TeamNotExistHTTPException(TeamManagerHTTPException):
    status_code = 404
    detail = "Пока еще не создана ни одна команда"

class MemberRoleUpdateHTTPException(TeamManagerHTTPException):
    status_code = 404
    detail = "Ошибка с базой данных. Не удалось обновить роль"