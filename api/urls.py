from django.urls import path, include
from rest_framework import routers
from api import views
from .views import TareaListCreateView, TareaRetrieveUpdateDestroyView
from .views import RegisterAndGetTokenView
from .views import LoginView

router = routers.DefaultRouter() # este elemento enrutador permite manejar múltiples rutas.
# esta es la base del conjunto de rutas o la raíz de las rutas
# acá se manejan las rutas o ENDsPOINTS que pueda tener tu API
router.register(r'programmers', views.ProgrammerViewSet)
# la r permite que no se interprete como un salto de línea o como un escape de carácter
# usamos la r para indicar que no tome los caracteres como \n o \t que es un salto de línea o una tabulación, es un formato tipo RAW de python.
# 'programmers' es un ENDPOINT
urlpatterns = [  
    path('', include(router.urls)),
    path('tareas/', TareaListCreateView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaRetrieveUpdateDestroyView.as_view(), name='tarea-retrieve-update-destroy'),
    path('register/', RegisterAndGetTokenView.as_view(), name='register_and_token'),
    path('login/', LoginView.as_view(), name='login'),
]
