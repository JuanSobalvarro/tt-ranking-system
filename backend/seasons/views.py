from rest_framework import viewsets
from .models import Season
from .serializers import SeasonSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def season_for_date(request):
    """
    Given a date, return the season that the date falls within
    :param:
    :return:
    """
    try:
        season = Season.get_season_for_datetime(request.query_params.get('date'))
        return Response(SeasonSerializer(season).data)
    except Season.DoesNotExist:
        return None

class SeasonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all().order_by('-start_date')
    serializer_class = SeasonSerializer
    pagination_class = SeasonPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
