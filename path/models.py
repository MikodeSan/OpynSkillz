from django.db import models
# from django.contrib.auth import get_user_model


class ZPath(models.Model):
    # code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.TextField('Complete', default='', blank=True)
    
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)


class ZContentSource(models.Model):
    identifier = models.CharField('ID', max_length=256, default='')
    etag = models.CharField('Etag', max_length=256, default='')
    label = models.CharField('Label', max_length=256, default='')
    url = models.URLField('URL', default='', blank=True)

    description = models.TextField('Description', default='', blank=True)
    published_t = models.DateTimeField('Published', blank=True, null=True)
    thumbnail_url = models.URLField('Thumbnail URL', default='', blank=True)
    country = models.CharField('Country', max_length=7, default='')
    is_4_kid = models.BooleanField('Pour enfant', default=False)

    n_view = models.IntegerField('Nombre de vues', default=0)
    n_subscriber = models.IntegerField('Nombre d\'abonnés', default=0)
    n_content = models.IntegerField('Nombre de contenus', default=0)

    paths = models.ManyToManyField('ZPath', related_name='sources', blank=True)       # through='ZCategory_Product'


class ZContent(models.Model):       # lesson / post

    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False, blank=True, null=False)
    url = models.URLField('URL', default='', blank=True, null=False)

    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

