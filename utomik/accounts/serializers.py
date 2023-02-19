from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    birthday = serializers.DateField(format='%Y-%m-%d')

    def validate_birthday(self, value):
        if value and value > (datetime.date.today() - datetime.timedelta(days=365*18)):
            raise ValidationError(_('User must be 18 years or older.'))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'birthday']
