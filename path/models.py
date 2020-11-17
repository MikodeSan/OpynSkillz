from django.db import models
# from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from mptt.models import MPTTModel, TreeForeignKey


# # A base model for the tree:

# class BaseTreeNode(PolymorphicMPTTModel):
#     parent = PolymorphicTreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name=_('parent'))
#     title = models.CharField(_("Title"), max_length=200)

#     class Meta(PolymorphicMPTTModel.Meta):
#         verbose_name = _("Tree node")
#         verbose_name_plural = _("Tree nodes")


# class ZPathNode(BaseTreeNode):
#     opening_title = models.CharField(_("Opening title"), max_length=200)
#     opening_image = models.ImageField(_("Opening image"), upload_to='images')

#     class Meta:
#         verbose_name = _("Category node")
#         verbose_name_plural = _("Category nodes")


# class TextNode(BaseTreeNode):
#     extra_text = models.TextField()

#     # Extra settings:
#     can_have_children = False

#     class Meta:
#         verbose_name = _("Text node")
#         verbose_name_plural = _("Text nodes")


# class ImageNode(BaseTreeNode):
#     image = models.ImageField(_("Image"), upload_to='images')

#     class Meta:
#         verbose_name = _("Image node")
#         verbose_name_plural = _("Image nodes")


class ZPathNode(MPTTModel):
    # code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    label = models.CharField('Label', max_length=256, default='', blank=True)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False)
    
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "PK: {} - {} - Complete: {}".format(self.pk, self.label, self.is_complete)

    # class MPTTMeta:
        # order_insertion_by = ['name']
        # pass


class ZPostNode(ZPathNode):

    # parent = TreeForeignKey('ZPathNode', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    pass


class ZContentNode(ZPathNode):

    # parent = TreeForeignKey('ZPostNode', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    pass


class Post(models.Model):
    title = models.CharField(max_length=120)
    path = TreeForeignKey('ZPathNode', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField('Content')
    slug = models.SlugField()
    pass

class ZSource(models.Model):
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
    n_content_public = models.IntegerField('Nombre de contenus détectés', default=0)
    
    paths = models.ManyToManyField('ZPathNode', related_name='sources', blank=True)       # through='ZCategory_Product'

    def __str__(self):
        return "Source {} - {}: {} content(s), {} subscriber(s)".format(self.identifier, self.label, self.n_content, self.n_subscriber)


class ZSourceYoutube(ZSource):

    pass


class ZSourceBlog(ZSource):

    pass


class ZContent(models.Model):       # lesson / post / YT video

    identifier = models.CharField('ID', max_length=256, default='')
    label = models.CharField('Label', max_length=256, default='', blank=False, null=False)
    description = models.TextField('Description', default='', blank=True)
    thumbnail_url = models.URLField('Thumbnail URL', default='', blank=True)
    published_t = models.DateTimeField('Published', auto_now=True, blank=True, null=True)

    is_complete = models.BooleanField('Complete', default=False, blank=True, null=False)
    url = models.URLField('URL', default='', blank=True, null=False)

    n_view = models.IntegerField('Nombre de vues', default=0)

    source = models.ForeignKey('ZSource', related_name='contents', on_delete=models.CASCADE, blank=True, null=True)
    # paths = models.ForeignKey('ZSource', related_name='contents', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Content {} - {}: {} view(s)".format(self.identifier, self.label, self.n_view)


class ZContentVideo(ZContent):       # lesson / post / YT video

    pass


class ZContentText(ZContent):       # lesson / post / YT video
    pass


class ZContentFile(ZContent):       # lesson / post / YT video
    pass

class ZContentLink(ZContent):       # lesson / post / YT video
    pass

class ZContentQuiz(ZContent):       # lesson / post / YT video
    pass

