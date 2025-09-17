from django.contrib import admin
from .models import Issue, Comment


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'state', 'priority', 'owner', 'date', 'expired_date']
    list_filter = ['state', 'priority', 'date', 'assignee']
    search_fields = ['title', 'description', 'owner__username']
    date_hierarchy = 'date'
    ordering = ['-date']

    fieldsets = (
        ('Informazioni Principali', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Assegnazione', {
            'fields': ('assignee', 'cc')
        }),
        ('Stato e Priorità', {
            'fields': ('state', 'priority', 'expired_date')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('owner').prefetch_related('assignee', 'cc')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post', 'name', 'created_on', 'active', 'body_preview']
    list_filter = ['active', 'created_on', 'name']
    search_fields = ['body', 'post__title', 'name__username']
    date_hierarchy = 'created_on'
    ordering = ['-created_on']

    def body_preview(self, obj):
        return obj.body[:100] + '...' if len(obj.body) > 100 else obj.body
    body_preview.short_description = 'Anteprima Commento'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('post', 'name')
