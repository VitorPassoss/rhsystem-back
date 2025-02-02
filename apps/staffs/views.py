from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.staffs.serializers import ProfissionaisSerializer, ProfissionalCreateSerializer, TurnoSerializer, StatusSerializer, EmpresaSerializer, CargoSerializer
from apps.staffs.models import Profissional, Turnos, Status, Empresas, Cargos

from django.db.models import Q  

class ProfissionaisView(APIView):
    serializer_class = ProfissionaisSerializer
    def get(self, request, id=None):
        if id:
            try:
                search_query = Profissional.objects.get(pk=id)
                search_item = self.serializer_class(search_query).data
                return Response(search_item, status=status.HTTP_200_OK)
            except Profissional.DoesNotExist:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        profissional_query = Profissional.objects.all()
        profissional = ProfissionaisSerializer(profissional_query, many=True ).data
        return Response(profissional, status=status.HTTP_200_OK)

    def post(self, request):
        serializer_item = ProfissionalCreateSerializer(data=request.data)
        if serializer_item.is_valid():
            serializer_item.save()
            return Response(serializer_item.data, status=status.HTTP_201_CREATED)
        return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        saved_supplie= get_object_or_404(Profissional.objects.all(), pk=id)
        serializer_item = ProfissionalCreateSerializer(instance=saved_supplie, data=request.data, partial=True)
        if serializer_item.is_valid():
            serializer_item.save()
            return Response(serializer_item.data, status=status.HTTP_200_OK)
        return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None):
        item = get_object_or_404(Profissional.objects.filter(pk=id))
        item.delete()
        return Response({"message": f"Product with id {id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    def post(self, request):
        search_string = request.data.get('search_string', '')

        if not search_string:
            return Response({"error": "search_string not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Use Q objects to perform case-insensitive search
        profissionais = Profissional.objects.filter(
            Q(nome__icontains=search_string) |
            Q(pis__icontains=search_string) |
            Q(jornada__icontains=search_string) |
            Q(cpf__icontains=search_string) |
            Q(contato_phone__icontains=search_string) |
            Q(contato_email__icontains=search_string)
        )

        serializer = ProfissionaisSerializer(profissionais, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TurnosView(APIView):
    serializer_class = TurnoSerializer
    def get(self, request, id=None):
        query = Turnos.objects.all()
        resp = self.serializer_class(query, many=True ).data
        return Response(resp, status=status.HTTP_200_OK)

class StatusView(APIView):
    serializer_class = StatusSerializer
    def get(self, request, id=None):
        query = Status.objects.all()
        resp = self.serializer_class(query, many=True ).data
        return Response(resp, status=status.HTTP_200_OK)

class EmpresaView(APIView):
    serializer_class = EmpresaSerializer
    def get(self, request, id=None):
        query = Empresas.objects.all()
        resp = self.serializer_class(query, many=True ).data
        return Response(resp, status=status.HTTP_200_OK)

class CargoView(APIView):
    serializer_class = CargoSerializer
    def get(self, request, id=None):
        query = Cargos.objects.all()
        resp = self.serializer_class(query, many=True ).data
        return Response(resp, status=status.HTTP_200_OK)