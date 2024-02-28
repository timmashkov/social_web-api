from sqladmin import ModelView

from models import Profile, ProfilePost, Friend


class ProfileAdmin(ModelView, model=Profile):
    column_list = [
        Profile.id,
        Profile.first_name,
        Profile.last_name,
        Profile.age,
        Profile.city,
        Profile.occupation,
        Profile.bio,
        Profile.friends,
    ]
    column_searchable_list = [Profile.first_name]
    column_sortable_list = [Profile.age]
    column_default_sort = [(Profile.id, True), (Profile.first_name, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class ProfilePostAdmin(ModelView, model=ProfilePost):
    column_list = [
        ProfilePost.id,
        ProfilePost.title,
        ProfilePost.hashtag,
        ProfilePost.text,
        ProfilePost.written_at,
        ProfilePost.author,
    ]
    column_searchable_list = [ProfilePost.title]
    column_sortable_list = [ProfilePost.written_at]
    column_default_sort = [(ProfilePost.id, True), (ProfilePost.written_at, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class ProfileFriendAdmin(ModelView, model=Friend):
    column_list = [Friend.id, Friend.profile_id, Friend.friend_id]
    column_searchable_list = [Friend.id]
    column_sortable_list = [Friend.id]
    column_default_sort = [(Friend.id, True), (Friend.profile_id, False)]

    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    can_export = True
