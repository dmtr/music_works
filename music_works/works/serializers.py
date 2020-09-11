from rest_framework import serializers

from works.models import MusicWork


class MusicWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicWork
        fields = ["iswc", "title", "contributors"]
