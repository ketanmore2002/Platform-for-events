# Generated by Django 4.1.1 on 2022-10-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0040_events_current_members_in_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='current_members_in_event',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]