from datetime import datetime
from rest_framework import serializers
from todo_list.models import ToDoList

class ToDoListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):    # user:id 로 보이던걸 user:email로 보이게 함
        return obj.user.pk

    class Meta:
        model = ToDoList
        fields = '__all__'


class ToDoListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ("title",)


class ToDoListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ("title", "is_complete", "completion_at")
    
    def update(self, instance, validated_data):
        # validated_data는 검증이 끝난 데이터
        if 'is_complete' in validated_data and validated_data['is_complete'] == True:
            # completion_at을 현재 시간으로 업데이트
            validated_data['completion_at'] = datetime.now()
        
        if 'is_complete' in validated_data and validated_data['is_complete'] == False:
            # is_complete가 false로 바뀌면 completion_at을 초기화
            validated_data['completion_at'] = None

        return super().update(instance, validated_data)


class ToDoListingSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj): 
        return obj.user.pk

    class Meta:
        model = ToDoList
        fields = ("pk", "title", "is_complete", "created_at", "updated_at", "completion_at", "user_id",)