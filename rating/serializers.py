from rest_framework import serializers
from rating.models import *

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('name', 'code')



class ModuleSerializer(serializers.ModelSerializer):
    teachers = ProfessorSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ('name', 'code', 'year', 'semester', 'teachers')





class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 250)
    password = serializers.CharField(max_length=250,write_only = True)

    class Meta:
        model = User
        fields =('username','password')



class RatingSerializer(serializers.ModelSerializer):
    professorid = serializers.CharField(max_length = 10)
    module_code = serializers.CharField(max_length =10)
    year = serializers.IntegerField()
    rating = serializers.IntegerField()

    class Meta:
        model = Rating
        fields = ('professorid','module_code', 'year', 'rating')
