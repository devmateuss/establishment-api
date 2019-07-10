from rest_framework.serializers import ModelSerializer
from .models import Estabeblishments


class EstablishmentsSerializer(ModelSerializer):

    class Meta:
        model = Estabeblishments
        fields = '__all__'