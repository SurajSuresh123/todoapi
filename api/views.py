from rest_framework import status
from rest_framework.views import APIView,Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Tasks
from django.contrib.auth.models import User
from .serializers import TaskSerializer,UserSerializer
import jwt,datetime

class register(APIView):
   def post(self,request):
      serializer=UserSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)

class login(APIView):
   def post(self,request):
      username=request.data['username']
      password=request.data['password']

      user=User.objects.filter(username=username).first()

      if user is  None:
        raise AuthenticationFailed('User not found')
      
      if not user.check_password(password):
        raise AuthenticationFailed('Incorrect Password')
      
      payload={
         'id':user.id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat':datetime.datetime.utcnow()
        }
      token =jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')

      response= Response()
      response.set_cookie(key='jwt',value=token,httponly=True)
      response.data={
          'jwt':token
      }
      return response

class userview(APIView):
   def get(self,request):
      token=request.COOKIES.get('jwt')
      if not token:
         raise AuthenticationFailed('Unauthenticated')
      
      try:
         payload=jwt.decode(token,'secret',algorithms=['HS256'])
      except jwt.ExpiredSignatureError:
         raise AuthenticationFailed('Unauthenticated')

      users=User.objects.filter(id=payload['id']).first()
      serializer1=UserSerializer(users)
      tasks=Tasks.objects.filter(user=payload['id'])
      serializer2=TaskSerializer(tasks,many=True)
      response=Response()
      response.data={
         'user':serializer1.data,
         'todo':serializer2.data
      }
      return response

class logout(APIView):
   def post(self,request):
      response=Response()
      response.delete_cookie('jwt')
      response.data={
         'message':"success"
      }
      return response

class createTodo(APIView):
   def post(self,request):
      token=request.COOKIES.get('jwt')
      if not token:
         raise AuthenticationFailed('Unauthenticated')
      try:
         payload=jwt.decode(token,'secret',algorithms=['HS256'])
      except jwt.ExpiredSignatureError:
         raise AuthenticationFailed('Unauthenticated')
      user = User.objects.filter(id=payload['id']).first()
      data=request.data.copy()
      data['user']=user.id
      serializer=TaskSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateTodo(APIView):
   def put(self,request,pk):
      token=request.COOKIES.get('jwt')
      if not token:
         raise AuthenticationFailed('Unauthenticated')
      task=Tasks.objects.get(id=pk)
      serializer=TaskSerializer(instance=task,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteTodo(APIView):
   def delete(self,request,pk):
      token=request.COOKIES.get('jwt')
      if not token:
         raise AuthenticationFailed('Unauthenticated')
      task=Tasks.objects.get(id=pk)
      task.delete()
      return Response('Item sucessfully delete!')
      
         

        
    

      

     
  

