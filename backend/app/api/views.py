from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import NoteSerializer
from app.models import Note
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    context = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = user.note_set.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def signUp(request):
    if User.objects.filter(username=request.data['username']):
        return Response({'message':f"@{request.data['username']} is already in use", 'status':'error'})
    if request.data['username'] == '' or len(request.data['username']) < 8:
        return Response({'message':"Username can't be null or less than 8 characters", 'status':'error'})
    if len(request.data['password']) < 8:
        return Response({'message':"Password must be more than 8 characters", 'status':'error'})
    if request.data['email'] == '':
        return Response({'message':"Enter a valid email", 'status':'error'})
    else:
        user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        user.save()
        return Response({'message':'Sign Up done, Login with your credentials', 'status':'success'})