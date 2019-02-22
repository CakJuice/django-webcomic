# Generated by Django 2.1.5 on 2019-02-13 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('slug', models.CharField(blank=True, db_index=True, max_length=70, null=True, verbose_name='Slug')),
                ('description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Description')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete='RESTRICT', related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete='RESTRICT', related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'db_table': 'cjwc_genre',
                'ordering': ['name'],
            },
        ),
    ]
