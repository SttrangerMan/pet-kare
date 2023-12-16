from django.urls import path
from .views import PetsViews

urlpatterns = [path("pets/", PetsViews.as_view())]
