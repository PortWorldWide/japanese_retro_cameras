from django.contrib import admin
from django import forms
from .models import Manufacturer, RecordingFormat, Camera, CameraImage, Documentation
from django.utils.html import format_html
import json

class CameraImageInline(admin.TabularInline):
    model = CameraImage
    extra = 1
    fields = ['image', 'caption', 'is_main']

class DocumentationInline(admin.TabularInline):
    model = Documentation
    extra = 1

class CameraAdminForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'
        widgets = {
            'specifications': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    form = CameraAdminForm
    list_display = ['name', 'manufacturer', 'release_year', 'recording_format', 'is_featured']
    list_filter = ['manufacturer', 'recording_format', 'release_year', 'is_featured']
    search_fields = ['name', 'description']
    inlines = [CameraImageInline, DocumentationInline]
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'manufacturer', 'release_year', 'recording_format')
        }),
        ('Характеристики', {
            'fields': ('specifications',)
        }),
        ('Описание', {
            'fields': ('description', 'features', 'is_featured')
        }),
    )

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(RecordingFormat)
class RecordingFormatAdmin(admin.ModelAdmin):
    list_display = ['name', 'format_type', 'slug']
    list_filter = ['format_type']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CameraImage)
class CameraImageAdmin(admin.ModelAdmin):
    list_display = ['camera', 'caption', 'is_main']
    list_filter = ['camera__manufacturer']

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ['camera', 'title', 'document_type']
    list_filter = ['document_type', 'camera__manufacturer']