from django.db.models import Sum
from rest_framework import serializers

from .models import Movie, Actor, Genre, Review, Rating


class CustomSerializer(serializers.ModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields'):
            return expanded_fields + self.Meta.extra_fields

        return expanded_fields


class FilterSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = ReviewSerializer(instance, context=self.context)
        return serializer.data


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for ActorViewSet
    """
    class Meta:
        model = Actor
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for GenreViewSet
    """
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(CustomSerializer):
    """
    Serializer for ReviewViewSet
    """
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterSerializer
        model = Review
        fields = '__all__'
        extra_fields = ['children']


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for ReviewViewSet
    """
    class Meta:
        model = Rating
        fields = '__all__'


class MovieSerializer(CustomSerializer):
    """
    Serializer for MovieViewSet
    """
    reviews = ReviewSerializer(many=True)
    ratings = RatingSerializer(many=True)
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        extra_fields = ['reviews', 'ratings', 'average_rating']

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(movie_id=obj.id)
        if len(ratings) > 0:
            return round(sum(rating.ranking_score for rating in ratings) / len(ratings), 1)
        return None

class StatisticsSerializer(serializers.Serializer):
    updated = serializers.DictField()
    recent = serializers.DictField()
