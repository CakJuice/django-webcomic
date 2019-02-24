# Generated by Django 2.1.7 on 2019-02-24 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import webcomic_site.comic.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('description', models.CharField(max_length=160, verbose_name='Description')),
                ('slug', models.CharField(blank=True, db_index=True, max_length=130, unique=True, verbose_name='Slug')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=webcomic_site.comic.models.upload_comic_thumbnail, verbose_name='Thumbnail')),
                ('banner', models.ImageField(blank=True, null=True, upload_to=webcomic_site.comic.models.upload_comic_banner, verbose_name='Banner')),
                ('state', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published'), (9, 'Archived')], default=0, verbose_name='State')),
                ('publish_date', models.DateTimeField(blank=True, null=True, verbose_name='Publish Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comics', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'db_table': 'cjwc_comic',
                'ordering': ['title'],
            },
        ),
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
        migrations.AddField(
            model_name='comic',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comics', to='comic.Genre', verbose_name='Genre'),
        ),
    ]
