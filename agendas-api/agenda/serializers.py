from rest_framework import serializers
from django.utils import timezone
from .models import Agenda

class AgendaSerializer(serializers.ModelSerializer):
    estado_display = serializers.SerializerMethodField(read_only=True)
    duracao_minutos = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Agenda
        fields = ['id', 'titulo', 'descricao', 'dataInicio', 'dataFim',
                  'local', 'estadoAtualAgenda', 'estado_display', 'duracao_minutos',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'estado_display', 'duracao_minutos']
    
    def get_estado_display(self, obj):
        """Retorna a versão legível do estado da agenda."""
        return dict(Agenda.ESTADO_CHOICES).get(obj.estadoAtualAgenda)
    
    def get_duracao_minutos(self, obj):
        """Calcula a duração da agenda em minutos."""
        if obj.dataInicio and obj.dataFim:
            delta = obj.dataFim - obj.dataInicio
            return int(delta.total_seconds() / 60)
        return None

    def validate(self, data):
        """Validações personalizadas para a agenda."""
        # Validação da data final posterior à data inicial
        if 'dataInicio' in data and 'dataFim' in data:
            if data['dataFim'] <= data['dataInicio']:
                raise serializers.ValidationError({
                    "dataFim": "A data de término deve ser posterior à data de início."
                })
        
        # Validação para impedir criação de agendas no passado
        if 'dataInicio' in data and not self.instance:  # Apenas para novas agendas
            now = timezone.now()
            if data['dataInicio'] < now:
                raise serializers.ValidationError({
                    "dataInicio": "Não é possível criar agendas com data de início no passado."
                })
        
        # Validação do estado da agenda
        if 'estadoAtualAgenda' in data:
            if data['estadoAtualAgenda'] not in dict(Agenda.ESTADO_CHOICES).keys():
                raise serializers.ValidationError({
                    "estadoAtualAgenda": "Estado inválido. Deve ser um dos seguintes: RECEBIDO, CONFIRMADO, ATENDIDO, CANCELADO"
                })
        
        return data
        
    def validate_titulo(self, value):
        """Validação específica para o título."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("O título deve ter pelo menos 3 caracteres.")
        return value