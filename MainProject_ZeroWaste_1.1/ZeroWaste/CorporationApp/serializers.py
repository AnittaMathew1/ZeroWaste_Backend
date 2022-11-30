from rest_framework import serializers

from .models import wastes

class wasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = wastes
        fields = ('__all__')