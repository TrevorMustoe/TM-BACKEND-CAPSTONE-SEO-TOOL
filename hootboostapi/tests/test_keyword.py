from rest_framework import status
from rest_framework.test import APITestCase
from hootboostapi.models import Keyword, User


class TestKeywords(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test class."""
        cls.user1 = User.objects.create(username="testuser1", company_name="Company A")
        cls.user2 = User.objects.create(username="testuser2", company_name="Company B")

        cls.keyword1 = Keyword.objects.create(target_keyword="SEO Strategy", user_id=cls.user1)
        cls.keyword2 = Keyword.objects.create(target_keyword="Backlinking", user_id=cls.user2)

    def test_create_keyword(self):
        """Test creating a new keyword."""
        new_keyword = {
            "target_keyword": "Content Marketing",
            "user_id": self.user1.id,
        }
        response = self.client.post("/keyword", new_keyword, format="json")

        print("Create Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["target_keyword"], new_keyword["target_keyword"])
        self.assertEqual(data["user_id"], new_keyword["user_id"])

        # Verify in DB
        db_keyword = Keyword.objects.get(pk=data["id"])
        self.assertEqual(db_keyword.target_keyword, new_keyword["target_keyword"])
        self.assertEqual(db_keyword.user_id.id, new_keyword["user_id"])

    def test_retrieve_keyword(self):
        """Test retrieving a single keyword by ID."""
        response = self.client.get(f"/keyword/{self.keyword1.id}")

        print("Retrieve Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.keyword1.id)
        self.assertEqual(data["target_keyword"], self.keyword1.target_keyword)
        self.assertEqual(data["user_id"], self.keyword1.user_id.id)

    def test_list_keywords(self):
        """Test listing all keywords."""
        response = self.client.get("/keyword")

        print("List Keywords Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)  # Should return 2 keywords

        first_keyword = data[0]
        self.assertTrue("id" in first_keyword)
        self.assertTrue("target_keyword" in first_keyword)
        self.assertTrue("user_id" in first_keyword)

    def test_update_keyword(self):
        """Test updating an existing keyword."""
        updated_keyword = {
            "target_keyword": "Updated SEO Strategy",
            "user_id": self.user2.id,
        }
        response = self.client.put(f"/keyword/{self.keyword1.id}", updated_keyword, format="json")

        print("Update Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        db_keyword = Keyword.objects.get(pk=self.keyword1.id)
        self.assertEqual(db_keyword.target_keyword, updated_keyword["target_keyword"])
        self.assertEqual(db_keyword.user_id.id, updated_keyword["user_id"])

    def test_delete_keyword(self):
        """Test deleting a keyword."""
        keyword_id = self.keyword2.id
        response = self.client.delete(f"/keyword/{keyword_id}")

        print("Delete Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        keywords = Keyword.objects.filter(id=keyword_id)
        self.assertEqual(len(keywords), 0)  # Keyword should be deleted
