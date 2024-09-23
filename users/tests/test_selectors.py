from django.test import TestCase
from uuid import uuid4
from unittest.mock import patch
from users.models import User
from users.selectors import UserSelector
from users.exceptions import UserNotFoundException


class UserSelectorTests(TestCase):
    def setUp(self):
        self.user_id = uuid4()
        self.user = User.objects.create(
            username="testuser", password="password"
        )

    def test_get_by_id_or_raise_success(self):
        user = UserSelector.get_by_id_or_raise(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_by_id_or_raise_failure(self):
        non_existent_user_id = uuid4()
        with self.assertRaises(UserNotFoundException):
            UserSelector.get_by_id_or_raise(non_existent_user_id)

    @patch("users.models.User.objects.get")
    def test_get_by_id_or_raise_calls_user_objects_get(self, mock_get):
        mock_get.return_value = self.user
        user = UserSelector.get_by_id_or_raise(self.user.id)
        self.assertEqual(user, self.user)
        mock_get.assert_called_once_with(id=self.user.id)
