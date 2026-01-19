"""Admin configuration for molecules app."""
from django.contrib import admin
from .models import SmilesQuery


@admin.register(SmilesQuery)
class SmilesQueryAdmin(admin.ModelAdmin):
    """Admin interface for SMILES queries."""
    
    list_display = ('smiles', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('smiles',)
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
