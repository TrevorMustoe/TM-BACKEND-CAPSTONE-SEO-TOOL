from rest_framework import status
from rest_framework.test import APITestCase
from hootboostapi.models import Audit_result, Website, User, Notes


class TestAuditResults(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test class."""
        cls.user1 = User.objects.create(username="testuser1", company_name="Company A")
        cls.user2 = User.objects.create(username="testuser2", company_name="Company B")

        cls.website1 = Website.objects.create(url="example.com", user_id=cls.user1)
        cls.website2 = Website.objects.create(url="testsite.com", user_id=cls.user2)

        cls.note1 = Notes.objects.create(note="Initial audit notes", user_id=cls.user1)
        cls.note2 = Notes.objects.create(note="Follow-up audit notes", user_id=cls.user2)

        cls.audit_result1 = Audit_result.objects.create(
            website_id=cls.website1,
            title_tag=True,  # ✅ Now using a Boolean value
            meta_desc_found=True,
            heading_tags_found=3,
            keyword_page_frequency=5,
            created_at="2024-03-01",
            score=85,
            audit_notes=cls.note1,
            user_id=cls.user1
        )

        cls.audit_result2 = Audit_result.objects.create(
            website_id=cls.website2,
            title_tag=False,  # ✅ Now using a Boolean value
            meta_desc_found=False,
            heading_tags_found=2,
            keyword_page_frequency=3,
            created_at="2024-02-15",
            score=75,
            audit_notes=cls.note2,
            user_id=cls.user2
        )

    def test_create_audit_result(self):
        """Test creating a new audit result."""
        new_audit_result = {
            "website_id": self.website1.id,
            "title_tag": True,  # ✅ Using Boolean value
            "meta_desc_found": True,
            "heading_tags_found": 4,
            "keyword_page_frequency": 6,
            "created_at": "2024-03-05",
            "score": 90,
            "audit_notes_id": self.note1.id,
            "user_id": self.user1.id,
        }
        response = self.client.post("/audit_result", new_audit_result, format="json")

        print("Create Audit Result Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["title_tag"], new_audit_result["title_tag"])
        self.assertEqual(data["meta_desc_found"], new_audit_result["meta_desc_found"])

    def test_retrieve_audit_result(self):
        """Test retrieving a single audit result by ID."""
        response = self.client.get(f"/audit_result/{self.audit_result1.id}")

        print("Retrieve Audit Result Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.audit_result1.id)
        self.assertEqual(data["title_tag"], self.audit_result1.title_tag)  # ✅ Should be True or False
        self.assertEqual(data["meta_desc_found"], self.audit_result1.meta_desc_found)

    def test_list_audit_results(self):
        """Test listing all audit results."""
        response = self.client.get("/audit_result")

        print("List Audit Results Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)  # Should return 2 audit results

        first_audit_result = data[0]
        self.assertTrue("id" in first_audit_result)
        self.assertTrue(isinstance(first_audit_result["title_tag"], bool))  # ✅ Ensures it is Boolean
        self.assertTrue("meta_desc_found" in first_audit_result)

    def test_update_audit_result(self):
        """Test updating an existing audit result."""
        updated_audit_result = {
            "website_id": self.website2.id,
            "title_tag": False,  # ✅ Using Boolean value
            "meta_desc_found": True,
            "heading_tags_found": 5,
            "keyword_page_frequency": 2,
            "created_at": "2024-03-10",
            "score": 95,
            "audit_notes": self.note2.id,
            "user_id": self.user2.id,
        }
        response = self.client.put(f"/audit_result/{self.audit_result1.id}", updated_audit_result, format="json")

        print("Update Audit Result Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        db_audit_result = Audit_result.objects.get(pk=self.audit_result1.id)
        self.assertEqual(db_audit_result.title_tag, updated_audit_result["title_tag"])  # ✅ Boolean
        self.assertEqual(db_audit_result.meta_desc_found, updated_audit_result["meta_desc_found"])

    def test_delete_audit_result(self):
        """Test deleting an audit result."""
        audit_result_id = self.audit_result2.id
        response = self.client.delete(f"/audit_result/{audit_result_id}")

        print("Delete Audit Result Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        audit_results = Audit_result.objects.filter(id=audit_result_id)
        self.assertEqual(len(audit_results), 0)  # Audit result should be deleted
