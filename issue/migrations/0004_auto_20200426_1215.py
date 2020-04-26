# Generated by Django 2.2.7 on 2020-04-26 10:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issue', '0003_auto_20200415_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='cc',
            field=models.ManyToManyField(blank=True, related_name='cc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ManyToManyField(related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.IntegerField(choices=[(0, '----'), (1, 'Bassa'), (2, 'Media'), (3, 'Alta')], default=2),
        ),
    ]
