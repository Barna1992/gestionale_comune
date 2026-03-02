import os

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

STATUS_CHOICES = (
    (1, _("Inserita")),
    (2, _("Presa in carico")),
    (3, _("Risolta")),
    (4, _("Riaperta")),
    (5, _("Da verificare")),
)

RELEVANCE_CHOICES = (
    (0, "----"),
    (1, _("Bassa")),
    (2, _("Media")),
    (3, _("Alta")),
)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#0d6efd')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Issue(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignee = models.ManyToManyField(User, related_name='assigned_issues')
    cc = models.ManyToManyField(User, related_name='cc_issues', blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='owned_issues',
        null=True, blank=True,
    )
    description = models.TextField()
    state = models.IntegerField(choices=STATUS_CHOICES, default=1)
    priority = models.IntegerField(choices=RELEVANCE_CHOICES, default=2)
    expired_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='issues',
    )

    def __str__(self):
        return f'#{self.pk} - {self.title} ({self.get_state_display()})'

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'pk': self.pk})

    def priority_verbose(self):
        return dict(RELEVANCE_CHOICES)[self.priority]

    def state_verbose(self):
        return dict(STATUS_CHOICES)[self.state]


def attachment_upload_path(instance, filename):
    return f'attachments/issue_{instance.issue.pk}/{filename}'


class Attachment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=attachment_upload_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{os.path.basename(self.file.name)} - Issue #{self.issue.pk}'

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def is_image(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        return ext in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')


class Comment(models.Model):
    post = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner_comments',
        null=True, blank=True,
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        body_preview = self.body[:50] + '...' if len(self.body) > 50 else self.body
        return f'Commento di {self.name} su #{self.post.pk}: {body_preview}'
