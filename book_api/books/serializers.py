from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    genre = serializers.CharField(max_length=100, required=False, allow_blank=True)
    published_year = serializers.IntegerField(required=False, allow_null=True)
    isbn = serializers.CharField(max_length=20, required=False, allow_blank=True)