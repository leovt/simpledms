from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/<uuid:document_id>/', views.document, name='document'),
    path('docs/<uuid:document_id>/page<int:page>', views.page_image(100), name='preview'),
    path('docs/<uuid:document_id>/page<int:page>sm', views.page_image(10), name='thumbnail'),
    path('tags/add', views.addtag, name='addtag'),
]
