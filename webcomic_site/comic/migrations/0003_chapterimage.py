# Generated by Django 2.1.7 on 2019-03-10 13:12

from django.db import migrations, models
import django.db.models.deletion
import webcomic_site.comic.models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0002_comicchapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=webcomic_site.comic.models.upload_chapter_image, verbose_name='Image')),
                ('sequence', models.IntegerField(default=1, verbose_name='Sequence')),
                ('upload_at', models.DateTimeField(auto_now_add=True, verbose_name='Upload At')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='comic.ComicChapter', verbose_name='Chapter')),
            ],
            options={
                'ordering': ['sequence'],
            },
        ),
    ]
