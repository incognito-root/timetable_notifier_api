from rest_framework import serializers

class SectionSerializer(serializers.Serializer):
    section = serializers.CharField(max_length=100)
