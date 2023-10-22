import json

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from backend.settings import BASE_DIR
from .models import Movie, Actor, Genre, Review, Rating
from .permissions import IsStaffOrSafeMethodsPermission, IsOwnerOrReadAndCreateOnly
from .serializers import MovieSerializer, ActorSerializer, GenreSerializer, ReviewSerializer, RatingSerializer, \
    StatisticsSerializer
from .mixins import EnablePATCHMethodMixin
from .paginations import StandardPagination
from .filters import ActorFilter, MovieFilter


class MovieViewSet(EnablePATCHMethodMixin, viewsets.ModelViewSet):
    """
    ViewSet to work with movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsStaffOrSafeMethodsPermission, permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter


class ActorViewSet(EnablePATCHMethodMixin, viewsets.ModelViewSet):
    """
    ViewSet to work with actors and directors
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsStaffOrSafeMethodsPermission, permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ActorFilter


class GenreViewSet(EnablePATCHMethodMixin, viewsets.ModelViewSet):
    """
    ViewSet to work with genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrSafeMethodsPermission]
    pagination_class = StandardPagination


class ReviewViewSet(EnablePATCHMethodMixin, viewsets.ModelViewSet):
    """
    ViewSet to work with review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadAndCreateOnly, permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination


class RatingViewSet(EnablePATCHMethodMixin, viewsets.ModelViewSet):
    """
    ViewSet to work with rating
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadAndCreateOnly, permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination


class StatisticsView(viewsets.ViewSet):
    def list(self, request):
        with open('views_count.json', 'r') as f:
            json_data = json.load(f)

        serializer = StatisticsSerializer(data=json_data)
        if serializer.is_valid():
            Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        with open(BASE_DIR / 'views_count.json', 'r') as f:
            json_data = json.load(f)

        if pk not in json_data['recent'].keys():
            Response({'error': 'Invalid url'}, status=status.HTTP_400_BAD_REQUEST)

        views_count = json_data['updated'][pk]
        json_data['recent'][pk] += 1

        with open('views_count.json', 'w') as f:
            json.dump(json_data, f, indent=4, sort_keys=True)

        return Response({pk: views_count}, status=status.HTTP_200_OK)
