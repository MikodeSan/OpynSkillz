# Generated by Django 3.1.3 on 2020-11-19 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('path', '0005_auto_20201119_1206'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ZContentNode',
        ),
        migrations.CreateModel(
            name='ZContentNode',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('path.zpathnode',),
        ),
    ]
