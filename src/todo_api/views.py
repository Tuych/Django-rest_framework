from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.shortcuts import render, get_object_or_404
from .serializers import TodoSerializer, MovieSerializer
from .models import Todo, Movie
from .permissions import IsOwner
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework import mixins, status

#  rest_framework.views --- APIView

class TodoListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user=request.user)
        # todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, todo_id):
        try:
            todo_instance = Todo.objects.get(id=todo_id)
            if todo_instance.user != self.request.user:
                todo_instance = None
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

        if todo_instance.user != request.user:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response({"error":"todo id doesnt find"}, status=status.HTTP_400_BAD_REQUEST) 

        if todo_instance.user != request.user:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
         
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
        

# GenericApi view
class RetrieveDeleteItem(GenericAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CreateListItem(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class RetrieveUpdateDeleteItem(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin, 
                                mixins.DestroyModelMixin,
                                GenericAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

#Custome mixins (uzimizga moslab yozib oladigan mixinslar)
class MultipleFieldLookupMixin:

    def retrieve(self,request, *args, **kwargs):
        instance = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(instance) # darsdagi kodni to'g'irladik darsda (self.get_serializer(insrtance) yozilib ketgan
        return Response(serializer.data)



#Concreate views
class ListAPIItem(ListAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()



class MovieCreateItem(CreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class MovieListItem(ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
