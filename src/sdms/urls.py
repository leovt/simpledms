from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/<uuid:document_id>/', views.document, name='document'),
    path('docs/<uuid:document_id>/page<int:page>', views.page_image(100), name='preview'),
    path('docs/<uuid:document_id>/page<int:page>sm', views.page_image(10), name='thumbnail'),
    path('docs/all', views.DocumentListView.as_view()),
    path('inbox', views.InboxListView.as_view(), name="inbox"),
    path('holdfile', views.HoldfileListView.as_view(), name="holdfile"),
    path('archive', views.ArchiveListView.as_view(), name="archive"),
    path('search', views.SearchListView.as_view(), name="search"),
    path('upload', views.upload, name="upload"),
    path('tags/add', views.addtag, name='addtag'),
    path('media/<str:path>', views.media, name='media'),
]
