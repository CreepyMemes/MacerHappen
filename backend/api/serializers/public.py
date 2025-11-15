from rest_framework import serializers
from ..utils import(
    GetCategoriesMixin
)

class GetCategoriesSerializer(GetCategoriesMixin, serializers.Serializer):
    """
    Public: Returns all categories.
    """
    def to_representation(self, validated_data):
        return {
            "categories": self.get_categories_public()
        }

