from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Estabeblishments
from .serializers import EstablishmentsSerializer
from geopy.distance import geodesic
import requests
import json


class EstabeblishmentsViewSet(ModelViewSet):
    serializer_class = EstablishmentsSerializer
    queryset = Estabeblishments.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        adreess = str(data['street']) + ',' + str(data['number']) + ',' + str(data['neighborhood']) + ',' + str(data['city']) + ',' + str(data['state'])
        r = requests.get('http://nominatim.openstreetmap.org/search?email=op.mateusinfo@gmail.com&format=json&q=[%s]' % adreess)
        r.headers['content-type']

        content = json.loads(r.content)

        print(content)

        if len(content) > 0:
            Estabeblishments.objects.create(
                name=data['name'],
                street=data['street'],
                number=int(data['number']),
                neighborhood=data['neighborhood'],
                state=data['state'],
                city=data['city'],
                latitude=float(content[0]['lat']),
                longitude=float(content[0]['lon']),
            )

            return JsonResponse({
                'success': True,
            })
        else:
            return JsonResponse({
                'success': False,
                'message': "Endereço não localizado"
            })

    @action(methods=["POST"], detail=False)
    def list_estabeblishment(self, request):
        data = request.data
        estabeblishments = Estabeblishments.objects.all()

        list_estabeblishments = []

        for item in estabeblishments:
            coord1 = (item.latitude, item.longitude)
            coord2 = (data['latitude'], data['longitude'])

            distance = geodesic(coord1, coord2).meters

            if distance <= data['fance']:

                list_estabeblishments.append(item)

        list_estabeblishments = self.serializer_class(list_estabeblishments, many=True)

        return Response(list_estabeblishments.data)