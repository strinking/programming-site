# Generated by Django 2.0.7 on 2019-06-02 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0008_remove_editable_false_on_guide_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
