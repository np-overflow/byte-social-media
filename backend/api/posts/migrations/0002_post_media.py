# Generated by Django 2.1.3 on 2018-11-11 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='posts.Media'),
        ),
    ]
