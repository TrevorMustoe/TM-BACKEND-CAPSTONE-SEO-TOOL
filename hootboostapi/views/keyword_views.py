"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import Keyword


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
                
class KeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Keyword
        fields = ('id', 'target_keyword', 'user_id')