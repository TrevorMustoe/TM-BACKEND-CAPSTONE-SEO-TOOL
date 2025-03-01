"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import User


class UserView(ViewSet):
    """HootBoost User view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user info

        Returns:
            Response -- JSON serialized user info
        """
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all user info

        Returns:
            Response -- JSON serialized list of user info
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        user = User.objects.create(
            username=request.data["username"],
            company_name=request.data["company_name"],
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)
                
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'company_name')