from sqladmin import ModelView

from models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.login, User.email, User.phone_number, User.is_verified]
    column_details_exclude_list = [User.password, User.token, User.profile_link]
    column_searchable_list = [User.login]
    column_sortable_list = [User.id]
    column_default_sort = [(User.email, True), (User.login, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
