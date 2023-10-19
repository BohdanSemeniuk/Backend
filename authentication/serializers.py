from django.contrib.auth import authenticate
from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        username = data['username']
        password = data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError('User not found')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')

        return {
            'username': username,
            'password': password
        }

    def to_representation(self, instance):
        return {
            'user': {
                'id': instance['user'].id,
                'username': instance['user'].username,
            },
            'token': instance['token']
        }

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return {'user': user, 'token': token[0].key}

        raise serializers.ValidationError('Invalid login credentials')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

    def create(self, validated_data):
        res = {}
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        res['username'], res['password'], res['token'] = \
            user.username, user.password, Token.objects.get_or_create(user=user)[0].key
        return res
