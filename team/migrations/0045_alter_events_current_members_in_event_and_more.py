# Generated by Django 4.1.1 on 2022-10-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0044_alter_teams_name_of_members_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='current_members_in_event',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='number_of_members_allowed_in_event',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]