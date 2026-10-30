from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryPhoto
from database.admin import publish_in_gallery, unpublish_from_gallery


class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption', 'show_in_gallery', 'image_preview')
    list_editable = ('caption', 'show_in_gallery')
    search_fields = ('caption',)
    actions = [publish_in_gallery, unpublish_from_gallery]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px; max-width:150px;" />', 
                obj.thumbnail.url)
        return '-'

    def animal_name(self, obj):
        if obj.animal:
            return obj.animal.name
        return '—'

admin.site.register(GalleryPhoto, GalleryPhotoAdmin)