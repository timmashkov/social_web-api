from sqladmin import ModelView

from models import Group, GroupPost


class GroupAdmin(ModelView, model=Group):
    column_list = [
        Group.id,
        Group.title,
        Group.description,
        Group.is_official,
        Group.created_at,
        Group.group_admin,
        Group.subscribers,
        Group.group_posts,
    ]
    column_searchable_list = [Group.title]
    column_sortable_list = [Group.created_at]
    column_default_sort = [(Group.subscribers, True), (Group.title, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class GroupPostAdmin(ModelView, model=GroupPost):
    column_list = [
        GroupPost.id,
        GroupPost.header,
        GroupPost.hashtag,
        GroupPost.body,
        GroupPost.written_at,
        GroupPost.group_author,
        GroupPost.community,
    ]
    column_searchable_list = [GroupPost.header]
    column_sortable_list = [GroupPost.written_at]
    column_default_sort = [(GroupPost.id, True), (GroupPost.written_at, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
