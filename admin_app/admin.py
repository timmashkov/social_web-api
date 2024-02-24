from sqladmin import Admin

from admin_app.admin_views import UserAdmin, ProfileAdmin
from configuration.core.database import connector
from configuration.server import ApiServer


admin = Admin(ApiServer.app_auth, connector.engine)


admin.add_view(UserAdmin)
admin.add_view(ProfileAdmin)
