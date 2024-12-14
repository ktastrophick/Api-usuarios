# from django.shortcuts import render <-- esta libreria no la usamos por ahora
# from django.shortcuts import render <-- esta libreria no la usamos por ahora
from rest_framework import viewsets
from .serializer import ProgrammerSerializer
from .models import programmer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tarea
from .serializer import TareaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Permitir que cualquier usuario no autenticado acceda a este endpoint

class TareaListCreateView(generics.ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

class TareaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

# Create your views here.
class ProgrammerViewSet(viewsets.ModelViewSet):
    queryset = programmer.objects.all()
    serializer_class = ProgrammerSerializer

class RegisterAndGetTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario
        user = User.objects.create_user(username=username, password=password, email=email)

        # Generar tokens para el usuario registrado
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
