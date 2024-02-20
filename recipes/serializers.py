# Rest Framework
from rest_framework import serializers

# Models
from .models import Category, Recipe
from django.contrib.auth.models import User
from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug',]


# Classe Serializadora
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public', 'author', 
            'author_name', 'category', 'category_name', 'preparation',
            'tags', 'tag_objects', 'tag_links'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name='get_preparation', read_only=True)

    category_name = serializers.StringRelatedField(source='category', read_only=True)
    author_name = serializers.StringRelatedField(source='author', read_only=True)

    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True, source='tags', read_only=True,
        view_name='recipes:recipes_api_v2_tag'
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'