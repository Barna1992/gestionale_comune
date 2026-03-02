from django.urls import path

from .views import (
    AttachmentDeleteView,
    DashboardView,
    IssueDeleteFormView,
    IssueDetailView,
    IssueEditFormView,
    IssueEditStateFormView,
    IssueFormView,
    IssueListView,
)

urlpatterns = [
    path('', IssueListView.as_view(), name='base'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('new/', IssueFormView.as_view(), name='create-issue'),
    path('<int:pk>/edit/', IssueEditFormView.as_view(), name='edit-issue'),
    path('<int:pk>/edit-state/', IssueEditStateFormView.as_view(), name='edit-issue-state'),
    path('<int:pk>/delete/', IssueDeleteFormView.as_view(), name='delete-issue'),
    path('attachment/<int:pk>/delete/', AttachmentDeleteView.as_view(), name='delete-attachment'),
]
