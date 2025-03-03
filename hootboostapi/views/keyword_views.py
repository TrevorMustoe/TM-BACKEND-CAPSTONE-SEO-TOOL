"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import Keyword, User


class KeywordView(ViewSet):
    """HootBoost Keyword view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single keyword info

        Returns:
            Response -- JSON serialized keyword info
        """
        keyword = Keyword.objects.get(pk=pk)
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all keyword info

        Returns:
            Response -- JSON serialized list of keyword info
        """
        keyword = Keyword.objects.all()
        serializer = KeywordSerializer(keyword, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        user = User.objects.get(id=request.data["user_id"])


        keyword = Keyword.objects.create(
            target_keyword=request.data["target_keyword"],
            user_id=user,
        )
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data)
      
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        keyword = Keyword.objects.get(pk=pk)
        keyword.target_keyword = request.data["target_keyword"]
        
        user = User.objects.get(pk=request.data["user_id"])
        keyword.user_id = user
        keyword.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    def destroy(self, request, pk):
        keyword = Keyword.objects.get(pk=pk)
        keyword.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
                
class KeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Keyword
        fields = ('id', 'target_keyword', 'user_id')