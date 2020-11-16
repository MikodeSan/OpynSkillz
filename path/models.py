from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# from django.contrib.auth import get_user_model


class ZPath(MPTTModel):
    # code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    label = models.CharField('Label', max_length=256, default='', blank=True)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False)
    
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "PK: {} - {} - Complete: {}".format(self.pk, self.label, self.is_complete)

    # class MPTTMeta:
    #     order_insertion_by = ['name']

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

    def __str__(self):
        return "Source {} - {}: {} content(s), {} subscriber(s)".format(self.identifier, self.label, self.n_content, self.n_subscriber)


class ZContent(models.Model):       # lesson / post / YT video

    identifier = models.CharField('ID', max_length=256, default='')
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)
    thumbnail_url = models.URLField('Thumbnail URL', default='', blank=True)
    published_t = models.DateTimeField('Published', auto_now=True, blank=True, null=True)

    is_complete = models.BooleanField('Complete', default=False, blank=True, null=False)
    url = models.URLField('URL', default='', blank=True, null=False)

    n_view = models.IntegerField('Nombre de vues', default=0)

    source = models.ForeignKey('ZContentSource', related_name='contents', on_delete=models.CASCADE, blank=True, null=True)
    # paths = models.ForeignKey('ZContentSource', related_name='contents', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Content {} - {}: {} view(s)".format(self.identifier, self.label, self.n_view)


# class ZContentVideo(models.Model):       # lesson / post / YT video

# class ZContentText(models.Model):       # lesson / post / YT video

# class ZContentFile(models.Model):       # lesson / post / YT video

