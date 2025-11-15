from rest_framework import serializers
# from ..utils import(
 
# )

class GetCategoriesSerializer(serializers.Serializer):
    """
    Public: Returns all categories.
    """
    def to_representation(self, validated_data):
        from ..models import Category

        categories = Category.objects.all().order_by("name")

        return {
            "categories": [
                {"id": c.id, "name": c.name}
                for c in categories
            ]
        }

