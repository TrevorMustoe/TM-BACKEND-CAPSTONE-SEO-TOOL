"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hootboostapi.models import Website, User


class WebsiteView(ViewSet):
    """HootBoost Website view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single website info

        Returns:
            Response -- JSON serialized website info
        """
        website = Website.objects.get(pk=pk)
        serializer = WebsiteSerializer(website)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all website info

        Returns:
            Response -- JSON serialized list of website info
        """
        website = Website.objects.all()
        serializer = WebsiteSerializer(website, many=True)
        return Response(serializer.data)
      
    def create(self, request):
          """Handle POST operations

          Returns
              Response -- JSON serialized game instance
          """
          user = User.objects.get(id=request.data["user_id"])


          website = Website.objects.create(
              url=request.data["url"],
              site_name=request.data["site_name"],
              user_id=user,
          )
          serializer = WebsiteSerializer(website)
          return Response(serializer.data)
        
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        website = Website.objects.get(pk=pk)
        website.url = request.data["url"]
        website.site_name = request.data["site_name"]
        
        user = User.objects.get(pk=request.data["user_id"])
        website.user_id = user
        website.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
                
class WebsiteSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Website
        fields = ('id', 'url', 'site_name', 'user_id')