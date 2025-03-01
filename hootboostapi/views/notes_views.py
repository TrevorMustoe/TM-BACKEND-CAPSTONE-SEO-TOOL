"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import Notes, User


class NotesView(ViewSet):
    """HootBoost Notes view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single notes info

        Returns:
            Response -- JSON serialized notes info
        """
        notes = Notes.objects.get(pk=pk)
        serializer = NotesSerializer(notes)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all notes info

        Returns:
            Response -- JSON serialized list of notes info
        """
        notes = Notes.objects.all()
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        user = User.objects.get(id=request.data["user_id"])


        notes = Notes.objects.create(
            note=request.data["note"],
            user_id=user,
        )
        serializer = NotesSerializer(notes)
        return Response(serializer.data)
                
class NotesSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Notes
        fields = ('id', 'note', 'user_id')