from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("upload/", views.upload_cyclones, name="upload"),
    path("freqStorms/", views.freq_storms, name="storms")
]