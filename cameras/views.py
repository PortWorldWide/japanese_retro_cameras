from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Camera, Manufacturer, RecordingFormat

def index(request):
    featured_cameras = Camera.objects.filter(is_featured=True)[:6]
    manufacturers = Manufacturer.objects.all()
    recording_formats = RecordingFormat.objects.all()
    
    context = {
        'featured_cameras': featured_cameras,
        'manufacturers': manufacturers,
        'recording_formats': recording_formats,
        'total_cameras': Camera.objects.count(),
    }
    return render(request, 'index.html', context)

def camera_detail(request, slug):
    camera = get_object_or_404(Camera, slug=slug)
    manufacturers = Manufacturer.objects.all()
    recording_formats = RecordingFormat.objects.all()
    
    context = {
        'camera': camera,
        'manufacturers': manufacturers,
        'recording_formats': recording_formats,
    }
    return render(request, 'camera_detail.html', context)

def camera_list(request):
    manufacturer_slug = request.GET.get('manufacturer')
    format_slug = request.GET.get('format')
    
    cameras = Camera.objects.all()
    
    if manufacturer_slug:
        cameras = cameras.filter(manufacturer__slug=manufacturer_slug)
    if format_slug:
        cameras = cameras.filter(recording_format__slug=format_slug)
    
    manufacturers = Manufacturer.objects.all()
    recording_formats = RecordingFormat.objects.all()
    
    context = {
        'cameras': cameras,
        'manufacturers': manufacturers,
        'recording_formats': recording_formats,
        'selected_manufacturer': manufacturer_slug,
        'selected_format': format_slug,
    }
    return render(request, 'camera_list.html', context)

def search_results(request):
    query = request.GET.get('q', '')
    cameras = Camera.objects.filter(
        Q(name__icontains=query) | 
        Q(manufacturer__name__icontains=query) |
        Q(description__icontains=query)
    ) if query else Camera.objects.none()
    
    manufacturers = Manufacturer.objects.all()
    recording_formats = RecordingFormat.objects.all()
    
    context = {
        'cameras': cameras,
        'query': query,
        'manufacturers': manufacturers,
        'recording_formats': recording_formats,
    }
    return render(request, 'search_results.html', context)