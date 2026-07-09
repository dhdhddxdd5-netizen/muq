"""
Views for dalal_project.
"""
from django.http import JsonResponse


def health(request):
    """Health check endpoint for Railway load balancer."""
    return JsonResponse({"status": "ok"}, status=200)

