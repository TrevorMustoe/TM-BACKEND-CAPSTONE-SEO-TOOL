from rest_framework import status
from rest_framework.test import APITestCase
from hootboostapi.models import User


class TestUsers(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test class."""
        cls.user1 = User.objects.create(username="testuser1", company_name="Company A")
        cls.user2 = User.objects.create(username="testuser2", company_name="Company B")

    def test_create_user(self):
        """Test creating a new user."""
        new_user = {
            "username": "newtestuser",
            "company_name": "Company C",
        }
        response = self.client.post("/user", new_user, format="json")

        print("Create User Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["username"], new_user["username"])
        self.assertEqual(data["company_name"], new_user["company_name"])

        # Verify in DB
        db_user = User.objects.get(pk=data["id"])
        self.assertEqual(db_user.username, new_user["username"])
        self.assertEqual(db_user.company_name, new_user["company_name"])

    def test_retrieve_user(self):
        """Test retrieving a single user by ID."""
        response = self.client.get(f"/user/{self.user1.id}")

        print("Retrieve User Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.user1.id)
        self.assertEqual(data["username"], self.user1.username)
        self.assertEqual(data["company_name"], self.user1.company_name)

    def test_list_users(self):
        """Test listing all users."""
        response = self.client.get("/user")

        print("List Users Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)  # Should return 2 users

        first_user = data[0]
        self.assertTrue("id" in first_user)
        self.assertTrue("username" in first_user)
        self.assertTrue("company_name" in first_user)

    def test_update_user(self):
        """Test updating an existing user."""
        updated_user = {
            "username": "updateduser",
            "company_name": "Updated Company",
        }
        response = self.client.put(f"/user/{self.user1.id}", updated_user, format="json")

        print("Update User Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        db_user = User.objects.get(pk=self.user1.id)
        self.assertEqual(db_user.username, updated_user["username"])
        self.assertEqual(db_user.company_name, updated_user["company_name"])

    def test_delete_user(self):
        """Test deleting a user."""
        user_id = self.user2.id
        response = self.client.delete(f"/user/{user_id}")

        print("Delete User Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        users = User.objects.filter(id=user_id)
        self.assertEqual(len(users), 0)  # User should be deleted
