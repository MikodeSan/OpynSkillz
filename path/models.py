from django.db import models
# from django.contrib.auth import get_user_model


class ZPath(models.Model):
    # code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.TextField('Complete', default='', blank=True)
    
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)



class ZContentSource(models.Model):
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    url = models.URLField('URL', default='', blank=True, null=False)

    description = models.TextField('Description', default='', blank=True)

    n_content = models.IntegerField('Nombre de contenus', default=0, blank=True, null=True)

class ZContent(models.Model):       # lesson / post

    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False, blank=True, null=False)
    url = models.URLField('URL', default='', blank=True, null=False)

    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)


