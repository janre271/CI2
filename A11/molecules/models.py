"""Models for the molecules application."""
from __future__ import annotations

from django.db import models


class SmilesQuery(models.Model):
    """Store SMILES queries with timestamps."""
    
    smiles = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'SMILES queries'
    
    def __str__(self):
        return f"{self.smiles} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
