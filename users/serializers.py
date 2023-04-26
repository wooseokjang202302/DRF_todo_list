from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):   # validate는 다수의 필드에 유효성검사를 시행한다
        email = data.get('email')
        password = data.get('password')

        if email and password:  # 이메일과 패스워드가 모두 입력되었을때
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('유저 정보가 일치하지 않습니다.')
        else:
            raise serializers.ValidationError('이메일과 패스워드는 필수 입력사항입니다.')

        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "name", "gender", "age", "introduction"]
        read_only_fields = ['email']    # 이메일은 수정할 수 없게 함

    # inctance는 업데이트 대상, validated_data는 업데이트하고자 하는 필드값들이 담긴 딕셔너리
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None) # 비밀번호는 pop으로 뽑아내 밑에서 따로 처리
        for (key, value) in validated_data.items():
            setattr(instance, key, value)   # 인스턴스(업데이트 대상)에 key와 value를 할당
        if password is not None:    # 비밀번호가 None이 아닐때만 수정
            instance.set_password(password)
        instance.save()
        return instance
