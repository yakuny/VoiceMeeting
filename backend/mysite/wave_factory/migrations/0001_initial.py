# Generated by Django 3.0.3 on 2020-02-12 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('uuid', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='')),
                ('result', models.TextField(default='null')),
            ],
        ),
    ]
