from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from api.models import *
import authApp.utils as ut

class UserCreateSerializer(UserCreateSerializer):

	class Meta(UserCreateSerializer.Meta):
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name')

	def validate_email(self, value):
		"""
		Check the email format
		"""
		if "@" not in value:
			raise serializers.ValidationError("Email should contain @", code=422)
		if "." not in value:
			raise serializers.ValidationError("Email should contain @", code=422)

	def create(self, validated_data):
		"""
		! Create method is not working properly
		"""
		strip = lambda x: ut.StripAndCapital(validated_data.get(x))

		validated_data['first_name'] = strip('first_name')
		validated_data['last_name'] = strip('last_name')

		return User.objects.create_user(**validated_data)
