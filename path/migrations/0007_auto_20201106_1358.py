# Generated by Django 3.1.2 on 2020-11-06 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('path', '0006_auto_20201101_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zcontent',
            name='parent',
        ),
        migrations.AddField(
            model_name='zcontent',
            name='identifier',
            field=models.CharField(default='', max_length=256, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='zcontent',
            name='n_view',
            field=models.IntegerField(default=0, verbose_name='Nombre de vues'),
        ),
        migrations.AddField(
            model_name='zcontent',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='path.zcontentsource'),
        ),
    ]
