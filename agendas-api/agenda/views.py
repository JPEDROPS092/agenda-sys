from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Agenda
from .serializers import AgendaSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.utils import timezone

class AgendaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar e editar agendas.
    """
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    @swagger_auto_schema(
        operation_description="Lista todas as agendas disponíveis",
        responses={200: AgendaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna os detalhes de uma agenda específica",
        responses={
            200: AgendaSerializer(),
            404: "Agenda não encontrada"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova agenda, garantindo que as datas estejam corretas",
        request_body=AgendaSerializer,
        responses={
            201: AgendaSerializer(),
            400: "Dados inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Cria uma nova agenda, garantindo que as datas estejam corretas.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description="Permite atualização completa de uma agenda",
        request_body=AgendaSerializer,
        responses={
            200: AgendaSerializer(),
            400: "Dados inválidos",
            404: "Agenda não encontrada"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Permite atualização parcial, incluindo o estado da agenda",
        request_body=AgendaSerializer(partial=True),
        responses={
            200: AgendaSerializer(),
            400: "Dados inválidos",
            404: "Agenda não encontrada"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Permite atualização parcial, incluindo o estado da agenda.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Remove uma agenda",
        responses={
            204: "Agenda removida com sucesso",
            404: "Agenda não encontrada"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Agenda.objects.all()
        
        # Filter by date
        date_str = self.request.query_params.get('date', None)
        if date_str:
            try:
                date_obj = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
                aware_datetime = timezone.make_aware(timezone.datetime.combine(date_obj, timezone.datetime.min.time()))
                queryset = queryset.filter(
                    Q(dataInicio__date=aware_datetime.date()) |
                    Q(dataFim__date=aware_datetime.date())
                )
            except ValueError:
                pass  # Ignore invalid date formats
        
        # Filter by estado (status)
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estadoAtualAgenda=estado)
        
        # Filter by search term (in titulo or descricao)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(descricao__icontains=search) |
                Q(local__icontains=search)
            )
            
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date_obj = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                start_datetime = timezone.make_aware(timezone.datetime.combine(start_date_obj, timezone.datetime.min.time()))
                queryset = queryset.filter(dataInicio__gte=start_datetime)
            except ValueError:
                pass
                
        if end_date:
            try:
                end_date_obj = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
                end_datetime = timezone.make_aware(timezone.datetime.combine(end_date_obj, timezone.datetime.max.time()))
                queryset = queryset.filter(dataFim__lte=end_datetime)
            except ValueError:
                pass
                
        return queryset
        
    @swagger_auto_schema(
        method='patch',
        operation_description="Atualiza o estado de uma agenda",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['estadoAtualAgenda'],
            properties={
                'estadoAtualAgenda': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['RECEBIDO', 'CONFIRMADO', 'ATENDIDO', 'CANCELADO']
                )
            }
        ),
        responses={
            200: AgendaSerializer(),
            400: "Estado inválido",
            404: "Agenda não encontrada"
        }
    )
    @action(detail=True, methods=['patch'], url_path='estado')
    def update_estado(self, request, pk=None):
        """Endpoint especial para atualizar apenas o estado da agenda."""
        instance = self.get_object()
        estado = request.data.get('estadoAtualAgenda')
        
        if not estado or estado not in dict(Agenda.ESTADO_CHOICES).keys():
            return Response(
                {"error": "Estado inválido. Deve ser um dos seguintes: RECEBIDO, CONFIRMADO, ATENDIDO, CANCELADO"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        instance.estadoAtualAgenda = estado
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)