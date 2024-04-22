from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.shortcuts import render, get_object_or_404
from .serializers import TodoSerializer
from .models import Todo
from .permissions import IsOwner

#  rest_framework.views --- APIView

class TodoListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # todos = Todo.objects.filter(user=request.user)
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, todo_id):
        try:
            todo_instance = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            todo_instance = None
        return todo_instance

    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response({"error":"todo id doesnt find"}, status=status.HTTP_400_BAD_REQUEST)  
          
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response({"error":"todo id doesnt find"}, status=status.HTTP_400_BAD_REQUEST)  
        
        serializer = TodoSerializer(instance=todo_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response({"error":"todo id doesnt find"}, status=status.HTTP_400_BAD_REQUEST)  
        todo_instance.delete()
        return Response({"message":"To do deleted"})
    
#  rest_framework.viewsets --- ViewSet

class TodoViewSet(ViewSet):
    queryset = Todo.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = TodoSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoSerializer(item)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None, *args, **kwargs):
        item_instance = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoSerializer(instance=item_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None, *args, **kwargs):
        item_instance = get_object_or_404(self.queryset, pk=pk)
        item_instance.delete()
        return Response({"message":"To do deleted"})
        