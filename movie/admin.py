from django.contrib import admin

from .models import Movie, Actor, Review, Rating, Genre

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Genre)
