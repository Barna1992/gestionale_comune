"""
Step 2/3: Populate categories and copy date -> created_at.
"""

from django.db import migrations


CATEGORIES = [
    ('Lavori Pubblici', 'Segnalazioni relative a lavori pubblici e manutenzione', '#0d6efd'),
    ('Anagrafe', 'Pratiche e segnalazioni relative all\'anagrafe', '#198754'),
    ('Polizia Locale', 'Segnalazioni per la Polizia Locale', '#dc3545'),
    ('Ragioneria', 'Questioni contabili e finanziarie', '#ffc107'),
    ('Segreteria', 'Pratiche di segreteria generale', '#6f42c1'),
    ('Urbanistica', 'Segnalazioni urbanistiche e edilizie', '#0dcaf0'),
    ('Servizi Sociali', 'Segnalazioni relative ai servizi sociali', '#fd7e14'),
    ('Altro', 'Altre segnalazioni non categorizzate', '#6c757d'),
]


def populate_categories(apps, schema_editor):
    Category = apps.get_model('issue', 'Category')
    for name, description, color in CATEGORIES:
        Category.objects.get_or_create(
            name=name,
            defaults={'description': description, 'color': color},
        )


def copy_date_to_created_at(apps, schema_editor):
    Issue = apps.get_model('issue', 'Issue')
    for issue in Issue.objects.all():
        if issue.date and not issue.created_at:
            Issue.objects.filter(pk=issue.pk).update(created_at=issue.date)


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0006_category_attachment_issue_schema'),
    ]

    operations = [
        migrations.RunPython(populate_categories, reverse_noop),
        migrations.RunPython(copy_date_to_created_at, reverse_noop),
    ]
