"""
Step 1/3: Add Category, Attachment models and new nullable fields on Issue.
"""

import issue.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issue', '0005_auto_20220817_1224'),
    ]

    operations = [
        # Create Category model
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('color', models.CharField(default='#0d6efd', max_length=7)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        # Create Attachment model
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=issue.models.attachment_upload_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='issue.issue')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        # Add nullable created_at and updated_at to Issue
        migrations.AddField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        # Add category FK to Issue (nullable)
        migrations.AddField(
            model_name='issue',
            name='category',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='issues',
                to='issue.category',
            ),
        ),
    ]
