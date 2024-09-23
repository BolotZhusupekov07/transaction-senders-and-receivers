from uuid import UUID

from users.exceptions import UserNotFoundException
from users.models import User


class UserSelector:

    @staticmethod
    def get_by_id_or_raise(user_id: UUID) -> User:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundException(f"User not found with id: {user_id}")
