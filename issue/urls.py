from django.urls import path
from django.views.generic import TemplateView
from issue.views import IssueListView, IssueDetailView, IssueFormView, IssueEditFormView, IssueDeleteFormView, \
    IssueEditStateFormView

urlpatterns = [
    path('', IssueListView.as_view(), name='base'),
    path('<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('new/', IssueFormView.as_view(), name='create-issue'),
    path('<int:pk>/edit/', IssueEditFormView.as_view(), name='edit-issue'),
    path('<int:pk>/edit-state/', IssueEditStateFormView.as_view(), name='edit-issue-state'),
    path('<int:pk>/delete/', IssueDeleteFormView.as_view(), name='delete-issue'),
]
