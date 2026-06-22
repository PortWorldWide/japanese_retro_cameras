from django.http import JsonResponse
from django.db.models import Q
from cameras.models import Camera

def search_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        cameras = Camera.objects.filter(
            Q(name__icontains=query) | 
            Q(manufacturer__name__icontains=query)
        )[:10]
        results = [
            {
                'name': f"{cam.manufacturer.name} {cam.name}",
                'url': f"/cameras/camera/{cam.slug}/",
                'year': cam.release_year,
                'format': cam.recording_format.name
            }
            for cam in cameras
        ]
    else:
        results = []
    
    return JsonResponse(results, safe=False)