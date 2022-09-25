from rest_framework import serializers

from complaints_app.models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'
