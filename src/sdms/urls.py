from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/<uuid:document_id>/', views.document, name='document'),
    path('docs/<uuid:document_id>/page<int:page>', views.preview, name='preview'),
]
