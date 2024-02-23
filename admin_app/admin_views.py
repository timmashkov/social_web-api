from flask import redirect, url_for
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required


class UserModelView(ModelView):
    column_list = ("login", "email", "phone_number", "is_verified")
    details_modal = True
    can_create = False
    can_delete = False
    can_view_details = True
    column_default_sort = 'is_verified'
    column_filters = ('login', 'is_verified')
    page_size = 10
    column_editable_list = ('is_verified', 'login')
    column_details_list = ("login", "email", "phone_number", "is_verified")
    form_widget_args = {
        'login': {
            'readonly': True
        },
        'email': {
            'readonly': True
        },
        'phone_number': {
            'readonly': True,
            'disabled': True
        },
        'is_verified': {
            'readonly': True
        },
        }

    @expose("/")
    def index_view(self):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        try:
            return super(UserModelView, self).index_view()
        except Exception as e:
            print("Error", e)

    @login_required
    def get_list_row_actions(self):
        actions = super(UserModelView, self).get_list_row_actions()
        if len(actions) > 1:
            actions.pop()
        return actions


class UserTypeModelView(ModelView):

    @expose('/')
    def index_view(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        try:
            return super(UserTypeModelView, self).index_view()
        except Exception as e:
            print('Error', e)

    @login_required
    def update_model(self, form, model):
        super().update_model(form, model)

    @login_required
    def create_model(self, form):
        super().create_model(form)

    @login_required
    def delete_model(self, model):
        super().delete_model(model)
