"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import Audit_result


class Audit_resultView(ViewSet):
    """HootBoost Audit_result view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single audit_result info

        Returns:
            Response -- JSON serialized audit_result info
        """
        audit_result = Audit_result.objects.get(pk=pk)
        serializer = Audit_resultSerializer(audit_result)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all audit_result info

        Returns:
            Response -- JSON serialized list of audit_result info
        """
        audit_result = Audit_result.objects.all()
        serializer = Audit_resultSerializer(audit_result, many=True)
        return Response(serializer.data)
                
class Audit_resultSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Audit_result
        fields = ('id', 'website_id', 'user_id', 'title_tag', 'meta_desc_found', 'heading_tags_found', 'keyword_page_frequency', 'created_at', 'score', 'audit_notes')