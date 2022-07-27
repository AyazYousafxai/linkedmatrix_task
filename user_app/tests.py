from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def test_block_user_ip(self):
        url = reverse("ip_user")
        for i in range(0, 6):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_user(self):
        url = reverse("group_user")
        for index, group in enumerate(
            zip(["Gold", "Silver", "Bronze", "No Group"], [10, 5, 2, 1])
        ):
            print(group)
            data = {
                "user_id": "test" + str(index),
                "user_type": group[0],
                "password": "test",
            }

            for i in range(0, group[1] + 1):
                response = self.client.post(url, data, format="json")
                if i >= group[1]:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

                else:
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
