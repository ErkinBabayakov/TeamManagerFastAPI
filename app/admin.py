from sqladmin import Admin, ModelView
from app.models import UserOrm
from app.database import engine

class UserAdmin(ModelView, model=UserOrm):
    column_list = [UserOrm.id, UserOrm.email, UserOrm.first_name, UserOrm.last_name, UserOrm.role, UserOrm.created_at]

def setup_admin(app):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    return admin