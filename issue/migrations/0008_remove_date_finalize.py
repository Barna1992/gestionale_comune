"""
Step 3/3: Remove old date field, update related_names, finalize owner on_delete.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issue', '0007_populate_data'),
    ]

    operations = [
        # Remove old date field
        migrations.RemoveField(
            model_name='issue',
            name='date',
        ),
        # Update created_at: remove null=True (data was populated)
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # Update owner: CASCADE -> SET_NULL
        migrations.AlterField(
            model_name='issue',
            name='owner',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='owned_issues',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        # Update assignee related_name
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ManyToManyField(
                related_name='assigned_issues',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        # Update cc related_name
        migrations.AlterField(
            model_name='issue',
            name='cc',
            field=models.ManyToManyField(
                blank=True,
                related_name='cc_issues',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
