import django_filters

from .models import Actor, Movie

class ActorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    url = django_filters.CharFilter(field_name='url', lookup_expr='icontains')

    class Meta:
        model = Actor
        fields = ['name', 'age', 'url']


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    django_filters.CharFilter(field_name='url', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['title', 'genre', 'country', 'actors', 'url']