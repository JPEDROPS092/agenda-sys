from django.contrib import admin
from .models import Agenda

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'dataInicio', 'dataFim', 'local', 'estadoAtualAgenda', 'created_at')
    list_filter = ('estadoAtualAgenda', 'dataInicio', 'created_at')
    search_fields = ('titulo', 'descricao', 'local')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'local')
        }),
        ('Datas', {
            'fields': ('dataInicio', 'dataFim')
        }),
        ('Estado', {
            'fields': ('estadoAtualAgenda',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
