from django.shortcuts import render

# Create your views here.
"""Markers view."""

from django.views.generic.base import TemplateView


class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"