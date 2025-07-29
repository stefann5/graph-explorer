from django.db import models
import json
import datetime

# Create your models here.
class Workspace(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique name globally
    data_source_plugin = models.CharField(max_length=100)
    data_source_file = models.CharField(max_length=500, blank=True, null=True)
    filters = models.JSONField(default=dict, blank=True)
    search = models.CharField(max_length=500, blank=True, null=True)
    view_type = models.CharField(max_length=20, default='simple', choices=[
        ('simple', 'Simple'),
        ('block', 'Block')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.data_source_plugin}"
    
    def save_current_state(self, filters=None, search=None, view_type=None):
        if filters is not None:
            self.filters = filters
        if search is not None:
            self.search = search
        if view_type is not None:
            self.view_type = view_type
        self.save()

    def get_state(self):
        return {
            'data_source_plugin': self.data_source_plugin,
            'data_source_file': self.data_source_file,
            'filters': self.filters,
            'search': self.search,
            'view_type': self.view_type
        }