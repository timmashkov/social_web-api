from sqladmin import Admin

from auth_microservice.admin_app.admin_auth import auth_backend
from auth_microservice.admin_app.admin_views import (
    UserAdmin,
    ProfileAdmin,
    ProfilePostAdmin,
    GroupPostAdmin,
    GroupAdmin,
    ProfileFriendAdmin
)
from configuration.core.database import connector
from configuration.server import ApiServer


admin = Admin(ApiServer.app_auth, connector.engine, authentication_backend=auth_backend)


admin.add_view(UserAdmin)
admin.add_view(ProfileAdmin)
admin.add_view(ProfilePostAdmin)
admin.add_view(GroupPostAdmin)
admin.add_view(GroupAdmin)
admin.add_view(ProfileFriendAdmin)
