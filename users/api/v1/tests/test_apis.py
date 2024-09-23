from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.exceptions import UserNotFoundException
from users.models import User


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="username", password="hashed_password"
        )

    @patch("users.api.v1.views.UserBalanceService.get")
    def test_get_user_balance__success(self, mock_get_balance):
        mock_get_balance.return_value = 1000

        url = reverse("user-balance", kwargs={"user_id": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"user_id": str(self.user.id), "balance": 1000}
        )

    @patch("users.api.v1.views.UserBalanceService.get")
    def test_get_user_balance__raises_error__when_user_not_found(
        self, mock_get_balance
    ):
        mock_get_balance.side_effect = UserNotFoundException()

        url = reverse("user-balance", kwargs={"user_id": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            {
                "message": UserNotFoundException.default_message,
                "error_code": UserNotFoundException.error_code,
            },
        )
