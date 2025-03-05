from rest_framework import status
from rest_framework.test import APITestCase
from hootboostapi.models import Notes, User


class TestNotes(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test class."""
        cls.user1 = User.objects.create(username="testuser1", company_name="Company A")
        cls.user2 = User.objects.create(username="testuser2", company_name="Company B")

        cls.note1 = Notes.objects.create(note="First Note", user_id=cls.user1)
        cls.note2 = Notes.objects.create(note="Second Note", user_id=cls.user2)

    def test_create_note(self):
        """Test creating a new note."""
        new_note = {
            "note": "This is a test note",
            "user_id": self.user1.id,
        }
        response = self.client.post("/note", new_note, format="json")

        print("Create Note Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["note"], new_note["note"])
        self.assertEqual(data["user_id"], new_note["user_id"])

        # Verify in DB
        db_note = Notes.objects.get(pk=data["id"])
        self.assertEqual(db_note.note, new_note["note"])
        self.assertEqual(db_note.user_id.id, new_note["user_id"])

    def test_retrieve_note(self):
        """Test retrieving a single note by ID."""
        response = self.client.get(f"/note/{self.note1.id}")

        print("Retrieve Note Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.note1.id)
        self.assertEqual(data["note"], self.note1.note)
        self.assertEqual(data["user_id"], self.note1.user_id.id)

    def test_list_notes(self):
        """Test listing all notes."""
        response = self.client.get("/note")

        print("List Notes Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)  # Should return 2 notes

        first_note = data[0]
        self.assertTrue("id" in first_note)
        self.assertTrue("note" in first_note)
        self.assertTrue("user_id" in first_note)

    def test_update_note(self):
        """Test updating an existing note."""
        updated_note = {
            "note": "Updated Note Content",
            "user_id": self.user2.id,
        }
        response = self.client.put(f"/note/{self.note1.id}", updated_note, format="json")

        print("Update Note Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        db_note = Notes.objects.get(pk=self.note1.id)
        self.assertEqual(db_note.note, updated_note["note"])
        self.assertEqual(db_note.user_id.id, updated_note["user_id"])

    def test_delete_note(self):
        """Test deleting a note."""
        note_id = self.note2.id
        response = self.client.delete(f"/note/{note_id}")

        print("Delete Note Response:", response.status_code, response.content)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify in DB
        notes = Notes.objects.filter(id=note_id)
        self.assertEqual(len(notes), 0)  # Note should be deleted
