__all__ = (
    "GroupAdmin",
    "GroupPostAdmin",
    "ProfileAdmin",
    "ProfilePostAdmin",
    "UserAdmin",
    "ProfileFriendAdmin",
)
from .groups import GroupAdmin, GroupPostAdmin
from .profile import ProfileAdmin, ProfilePostAdmin, ProfileFriendAdmin
from .user import UserAdmin
