# Generated by Django 2.2.7 on 2020-01-05 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0004_auto_20191123_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
