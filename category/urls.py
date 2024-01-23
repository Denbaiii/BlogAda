from django.urls import path, include
from .views import CategoryCreateListView, CategoryDetailView

# My urls here.

urlpatterns = [
    path('create/', CategoryCreateListView.as_view()),
    path('detail/<int:id>/', CategoryDetailView.as_view()),
]