from django.db import models
from django.contrib.auth.models import User
import json

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
    
    def __str__(self):
        return self.name

class RecordingFormat(models.Model):
    FORMAT_TYPES = [
        ('analog', 'Аналоговый'),
        ('digital', 'Цифровой'),
        ('optical', 'Оптический диск'),
        ('flash', 'Флеш-память'),
        ('hdd', 'Встроенный HDD'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название формата")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    format_type = models.CharField(max_length=20, choices=FORMAT_TYPES, verbose_name="Тип формата")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Формат записи"
        verbose_name_plural = "Форматы записи"
    
    def __str__(self):
        return self.name

class Camera(models.Model):
    # Основная информация
    name = models.CharField(max_length=200, verbose_name="Название модели")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    release_year = models.IntegerField(verbose_name="Год выпуска")
    
    # Форматы
    recording_format = models.ForeignKey(RecordingFormat, on_delete=models.CASCADE, verbose_name="Формат записи")
    
    # Характеристики в JSON
    specifications = models.JSONField(default=dict, verbose_name="Характеристики")
    
    # Описание
    description = models.TextField(verbose_name="Описание")
    features = models.TextField(blank=True, verbose_name="Особенности")
    
    # Мета-информация
    is_featured = models.BooleanField(default=False, verbose_name="Показать в избранном")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Видеокамера"
        verbose_name_plural = "Видеокамеры"
        ordering = ['-release_year']
    
    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"
    
    def get_main_image(self):
        """Возвращает основное или первое изображение камеры"""
        try:
            main_image = self.images.filter(is_main=True).first()
            if main_image:
                return main_image
            return self.images.first()
        except Exception:
            return None

class CameraImage(models.Model):
    camera = models.ForeignKey(Camera, related_name='images', on_delete=models.CASCADE, verbose_name="Камера")
    image = models.ImageField(upload_to='cameras/', verbose_name="Изображение")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")
    
    class Meta:
        verbose_name = "Изображение камеры"
        verbose_name_plural = "Изображения камер"

class Documentation(models.Model):
    camera = models.ForeignKey(Camera, related_name='documents', on_delete=models.CASCADE, verbose_name="Камера")
    title = models.CharField(max_length=200, verbose_name="Название документа")
    document = models.FileField(upload_to='documents/', verbose_name="Файл документа")
    document_type = models.CharField(max_length=50, choices=[
        ('manual', 'Инструкция'),
        ('specs', 'Технические характеристики'),
        ('brochure', 'Брошюра'),
        ('service', 'Сервисное руководство'),
    ], verbose_name="Тип документа")
    
    class Meta:
        verbose_name = "Документация"
        verbose_name_plural = "Документация"
    
    def __str__(self):
        return f"{self.camera.name} - {self.title}"