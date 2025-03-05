from rest_framework import status
from rest_framework.test import APITestCase
from hootboostapi.models import Audit_Result_Keyword, Keyword, Audit_result, User, Website, Notes


class TestAuditResultKeyword(APITestCase):

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
            title_tag=True,  # Boolean field
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
            title_tag=False,  # Boolean field
            meta_desc_found=False,
            heading_tags_found=2,
            keyword_page_frequency=3,
            created_at="2024-02-15",
            score=75,
            audit_notes=cls.note2,
            user_id=cls.user2
        )

        cls.keyword1 = Keyword.objects.create(target_keyword="SEO Strategy", user_id=cls.user1)
        cls.keyword2 = Keyword.objects.create(target_keyword="Backlinking", user_id=cls.user2)

        cls.audit_result_keyword1 = Audit_Result_Keyword.objects.create(
            keyword=cls.keyword1,
            audit_result=cls.audit_result1
        )

        cls.audit_result_keyword2 = Audit_Result_Keyword.objects.create(
            keyword=cls.keyword2,
            audit_result=cls.audit_result2
        )

    def test_create_audit_result_keyword(self):
        """Test creating a new audit_result_keyword."""
        new_audit_result_keyword = {
            "keyword_id": self.keyword1.id,
            "audit_result_id": self.audit_result2.id
        }
        response = self.client.post("/audit_result_keyword", new_audit_result_keyword, format="json")

        print("Create Audit Result Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["keyword"], new_audit_result_keyword["keyword_id"])
        self.assertEqual(data["audit_result"], new_audit_result_keyword["audit_result_id"])

    def test_retrieve_audit_result_keyword(self):
        """Test retrieving a single audit_result_keyword by ID."""
        response = self.client.get(f"/audit_result_keyword/{self.audit_result_keyword1.id}")

        print("Retrieve Audit Result Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.audit_result_keyword1.id)
        self.assertEqual(data["keyword"], self.audit_result_keyword1.keyword.id)
        self.assertEqual(data["audit_result"], self.audit_result_keyword1.audit_result.id)

    def test_list_audit_result_keywords(self):
        """Test listing all audit_result_keywords."""
        response = self.client.get("/audit_result_keyword")

        print("List Audit Result Keywords Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)  # Should return 2 audit_result_keyword records

        first_audit_result_keyword = data[0]
        self.assertTrue("id" in first_audit_result_keyword)
        self.assertTrue("keyword" in first_audit_result_keyword)
        self.assertTrue("audit_result" in first_audit_result_keyword)

    def test_update_audit_result_keyword(self):
        """Test updating an existing audit_result_keyword."""
        updated_audit_result_keyword = {
            "keyword": self.keyword2.id,  # Change keyword association
            "audit_result": self.audit_result1.id,  # Change audit result association
        }
        response = self.client.put(
            f"/audit_result_keyword/{self.audit_result_keyword1.id}",
            updated_audit_result_keyword,
            format="json"
        )

        print("Update Audit Result Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        db_audit_result_keyword = Audit_Result_Keyword.objects.get(pk=self.audit_result_keyword1.id)
        self.assertEqual(db_audit_result_keyword.keyword.id, updated_audit_result_keyword["keyword"])
        self.assertEqual(db_audit_result_keyword.audit_result.id, updated_audit_result_keyword["audit_result"])

    def test_delete_audit_result_keyword(self):
        """Test deleting an audit_result_keyword."""
        audit_result_keyword_id = self.audit_result_keyword2.id
        response = self.client.delete(f"/audit_result_keyword/{audit_result_keyword_id}")

        print("Delete Audit Result Keyword Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        audit_result_keywords = Audit_Result_Keyword.objects.filter(id=audit_result_keyword_id)
        self.assertEqual(len(audit_result_keywords), 0)  # Audit_Result_Keyword should be deleted
