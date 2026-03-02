from django.contrib import admin

from .models import Attachment, Category, Comment, Issue


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'description']
    search_fields = ['name']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'state', 'priority', 'category', 'owner', 'created_at', 'expired_date']
    list_filter = ['state', 'priority', 'category', 'created_at', 'assignee']
    search_fields = ['title', 'description', 'owner__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Informazioni Principali', {
            'fields': ('title', 'description', 'owner', 'category')
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
        return qs.select_related('owner', 'category').prefetch_related('assignee', 'cc')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'issue', 'filename', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['issue__title', 'description']
    raw_id_fields = ['issue']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('issue', 'uploaded_by')


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
