from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from . import models


# default is 10 pixels
MPTT_ADMIN_LEVEL_INDENT = 20


# # The common admin functionality for all derived models:

# class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
#     GENERAL_FIELDSET = (None, {
#         'fields': ('parent', 'title'),
#     })

#     base_model = models.BaseTreeNode
#     base_fieldsets = (
#         GENERAL_FIELDSET,
#     )


# # Optionally some custom admin code

# class TextNodeAdmin(BaseChildAdmin):
#     pass


# # Create the parent admin that combines it all:

# class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
#     base_model = models.BaseTreeNode
#     child_models = (
#         (models.ZPatNode, BaseChildAdmin),
#         (models.TextNode, TextNodeAdmin),  # custom admin allows custom edit/delete view.
#         (models.ImageNode, BaseChildAdmin),
#     )

#     list_display = ('title', 'actions_column',)

#     class Media:
#         css = {
#             'all': ('admin/treenode/admin.css',)
#         }


admin.site.register(models.ZTreeNode, DraggableMPTTAdmin)
admin.site.register(models.ZPath)


admin.site.register(models.ZPost)


admin.site.register(models.ZSource)
admin.site.register(models.ZYoutubeChannel)
admin.site.register(models.ZSourceBlog)


admin.site.register(models.ZContent)

admin.site.register(models.ZContentVideo)
admin.site.register(models.ZYoutubeVideo)

admin.site.register(models.ZContentText)

admin.site.register(models.ZContentFile)

admin.site.register(models.ZContentLink)

admin.site.register(models.ZContentQuiz)
