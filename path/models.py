from django.db import models
# from django.contrib.auth import get_user_model


class ZPath(models.Model):
    # code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.TextField('Description', default='', blank=True)
    
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)



class ZContent(models.Model):       # lesson / post

    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False, blank=True, null=False)
    url = models.URLField('Source URL', default='', blank=True, null=False)

    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

