from rest_framework import serializers
from .models import programmer
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = programmer
        # fields = ('fullname','languaje','is_active’) acá podemos traer cualquier atributo del modelo o campo
        fields = '__all__'
        # con la opción de '__all__' nos traemos todo para ver y tener acceso a todo el registro de cada programador
