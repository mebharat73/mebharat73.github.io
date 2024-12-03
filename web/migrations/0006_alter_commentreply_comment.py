# Generated by Django 5.1.3 on 2024-11-25 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='web.comment'),
        ),
    ]
