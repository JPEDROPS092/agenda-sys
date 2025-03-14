from rest_framework import serializers
from .models import Agenda

class AgendaSerializer(serializers.ModelSerializer):
    dataInicio = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ", 
        input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"],
        help_text="Data e hora de início do evento no formato ISO (Ex: 2025-03-13T14:30:00.000Z)"
    )
    dataFim = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ", 
        input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"],
        help_text="Data e hora de término do evento no formato ISO (Ex: 2025-03-13T16:30:00.000Z)"
    )
    titulo = serializers.CharField(
        help_text="Título da agenda"
    )
    descricao = serializers.CharField(
        help_text="Descrição detalhada do evento/agenda"
    )
    local = serializers.CharField(
        help_text="Local onde o evento será realizado"
    )
    estadoAtualAgenda = serializers.CharField(
        help_text="Estado atual da agenda (ex: 'agendado', 'cancelado', 'realizado', etc.)"
    )
      
    class Meta:
        model = Agenda
        fields = ['id', 'titulo', 'descricao', 'dataInicio', 'dataFim',
                  'local', 'estadoAtualAgenda', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Verifica se a data final é posterior à data inicial.
        """
        if 'dataInicio' in data and 'dataFim' in data:
            if data['dataFim'] <= data['dataInicio']:
                raise serializers.ValidationError({
                    "dataFim": "A data de término deve ser posterior à data de início."
                })
        return data