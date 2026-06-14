from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'service', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at', 'is_read']
