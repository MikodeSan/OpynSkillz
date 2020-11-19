from django.utils.translation import ugettext_lazy as _
from django.db import models
# from django.contrib.auth import get_user_model

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from mptt.models import MPTTModel, TreeForeignKey


class ZTreeNode(MPTTModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    slug = models.SlugField()


    # class MPTTMeta:
        # order_insertion_by = ['name']
        # pass


    def object_type(self):
        """
        docstring
        """
        # return self.content_object.__class__.__name__
        # return type(self.content_object)
        print(self.content_type, self.content_object)
        return self.content_type.model_class().__name__


class ZPath(models.Model):

    label = models.CharField('Label', max_length=256, default='', blank=True)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False)
    
    def __str__(self):
        return "PK: {} - {} - Complete: {}".format(self.pk, self.label, self.is_complete)


class ZPost(models.Model):

    label = models.CharField('Label', max_length=256, default='', blank=True)
    description = models.TextField('Description', default='', blank=True)

    is_complete = models.BooleanField('Complete', default=False)
    
    def __str__(self):
        return "PK: {} - {} - Complete: {}".format(self.pk, self.label, self.is_complete)

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
    
    paths = models.ManyToManyField('ZPath', related_name='sources', blank=True)       # through='ZCategory_Product'

    def __str__(self):
        return "Source {} - {}: {} content(s), {} subscriber(s)".format(self.identifier, self.label, self.n_content, self.n_subscriber)


class ZYoutubeChannel(ZSource):

    pass


class ZSourceBlog(ZSource):

    pass


class ZContent(models.Model):

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


class ZContentVideo(ZContent):

    pass


class ZYoutubeVideo(ZContentVideo):

    pass


class ZContentText(ZContent):
    pass


class ZContentFile(ZContent):
    pass

class ZContentLink(ZContent):
    pass

class ZContentQuiz(ZContent):
    pass



# # A base model for the tree:

# class BaseTreeNode(PolymorphicMPTTModel):
#     parent = PolymorphicTreeForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('parent'))
#     title = models.CharField(_("Title"), max_length=200)

#     class Meta(PolymorphicMPTTModel.Meta):
#         verbose_name = _("Tree node")
#         verbose_name_plural = _("Tree nodes")


# # Create 3 derived models for the tree nodes:

# class CategoryNode(BaseTreeNode):
#     opening_title = models.CharField(_("Opening title"), max_length=200)
#     opening_image = models.ImageField(_("Opening image"), upload_to='images')

#     # # Extra settings:
#     # can_have_children = True

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
