from django.db import models
# from django.contrib.auth import get_user_model


class ZPath(models.Model):
    # code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)
    
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
