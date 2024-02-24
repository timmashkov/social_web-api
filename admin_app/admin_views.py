from sqladmin import ModelView

from models import User, Profile


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


class ProfileAdmin(ModelView, model=Profile):
    column_list = [Profile.id, Profile.first_name, Profile.last_name, Profile.age, Profile.city,
                   Profile.occupation, Profile.bio]
    column_searchable_list = [Profile.first_name]
    column_sortable_list = [Profile.age]
    column_default_sort = [(Profile.id, True), (Profile.first_name, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
