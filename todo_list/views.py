from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from todo_list.models import ToDoList
from todo_list.serializers import ToDoListSerializer, ToDoListCreateSerializer, ToDoListingSerializer, ToDoListUpdateSerializer
from todo_list import messages

class ToDoListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message":messages.REQUIRED_LOGIN}, status=status.HTTP_401_UNAUTHORIZED)
        todo_list = ToDoList.objects.filter(user=request.user)  # 본인이 작성한 글만 가져온다
        serializer = ToDoListingSerializer(todo_list, many=True) # 복수의 객체를 시리얼화하기 때문에 many=True작성
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message":messages.REQUIRED_LOGIN}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ToDoListCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
            {"title":serializer.data.get('title'),
             "message":messages.SUCCESS_CREATE_LIST
            }, 
             status=status.HTTP_200_OK
        )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoListDetailView(APIView):
    def get(self, request, todo_list_id):
        if not request.user.is_authenticated:
            return Response({"message":messages.REQUIRED_LOGIN}, status=status.HTTP_401_UNAUTHORIZED)
        todo_list = get_object_or_404(ToDoList, id=todo_list_id)
        if request.user != todo_list.user:
            return Response({"message":messages.NOT_AUTHOR_VIEW}, status=status.HTTP_403_FORBIDDEN)
        serializer = ToDoListSerializer(todo_list)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, todo_list_id):
        todo_list = get_object_or_404(ToDoList, id=todo_list_id)
        if request.user == todo_list.user:    # 본인일 경우에만 글 수정
            serializer = ToDoListUpdateSerializer(todo_list, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":messages.NOT_HAVE_PERMISSION}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, todo_list_id):
        todo_list = get_object_or_404(ToDoList, id=todo_list_id)
        if request.user == todo_list.user:
            todo_list.delete()
            return Response({"message":messages.SUCCESS_DELETE_LIST}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":messages.NOT_HAVE_PERMISSION}, status=status.HTTP_403_FORBIDDEN)