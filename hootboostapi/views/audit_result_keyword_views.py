"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import Audit_Result_Keyword, Keyword, Audit_result


class Audit_Result_KeywordView(ViewSet):
    """HootBoost Audit_Result_Keyword view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single audit_result_keyword info

        Returns:
            Response -- JSON serialized audit_result_keyword info
        """
        audit_result_keyword = Audit_Result_Keyword.objects.get(pk=pk)
        serializer = Audit_Result_KeywordSerializer(audit_result_keyword)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all audit_result_keyword info

        Returns:
            Response -- JSON serialized list of audit_result_keyword info
        """
        audit_result_keyword = Audit_Result_Keyword.objects.all()
        serializer = Audit_Result_KeywordSerializer(audit_result_keyword, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
     
        keyword = Keyword.objects.get(id=request.data["keyword_id"])
        audit_result = Audit_result.objects.get(id=request.data["audit_result_id"])


        audit_result_keyword = Audit_Result_Keyword.objects.create(
            keyword=keyword,
            audit_result=audit_result
        )
        serializer = Audit_Result_KeywordSerializer(audit_result_keyword)
        return Response(serializer.data)
                
class Audit_Result_KeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Audit_Result_Keyword
        fields = ('id', 'keyword', 'audit_result')