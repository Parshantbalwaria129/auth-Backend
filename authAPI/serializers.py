from rest_framework import serializers
from .views import UserProfile


class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['firstName', 'lastName', 'secondEmail', 'phone', 'secondPhone',
                  'address', 'city', 'state', 'zipcode', 'country']
