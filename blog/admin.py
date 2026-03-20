from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Post, BlogImage
from django.conf import settings

MEDIA_URL = settings.MEDIA_URL


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class IsPublishedAdmin(admin.ModelAdmin):
    list_display = ('is_published',)
    list_editable = ('is_published',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('title',)


class CreatedAtAdmin(admin.ModelAdmin):
    list_display = ('created_at',)


class CategoryAdmin(IsPublishedAdmin, TitleAdmin):
    list_display = IsPublishedAdmin.list_display + TitleAdmin.list_display + (
        'slug',
    )
    list_editable = IsPublishedAdmin.list_editable
    inlines = (PostInline,)
    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)


class PostAdmin(IsPublishedAdmin, TitleAdmin, CreatedAtAdmin):
    list_display = (IsPublishedAdmin.list_display + TitleAdmin.list_display
                    + CreatedAtAdmin.list_display)

    list_display += (
        'author',
        'text',
        'category',
        'pub_date',
    )
    list_editable = IsPublishedAdmin.list_editable + (
        'text',
        'category',
        'pub_date',
    )
    list_display_links = ('title',)


class BlogImageAdmin(admin.ModelAdmin):
    list_display_links = ('image',)
    list_display = ('image', 'alt_text', 'uploaded_at',
                    'image_preview', 'full_url_display')
    list_editable = ('alt_text',)
    readonly_fields = ('image_preview', 'full_url_display')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px; max-width:150px;" />', 
                obj.image.url)
        return '-'

    image_preview.short_description = 'Превью'
    
    def full_url_display(self, obj):
        if obj.image:
            return f'{MEDIA_URL}{obj.image.name}'
        return "-"
    
    full_url_display.short_description = 'Полный URL'


admin.site.register(Post, PostAdmin)
admin.site.register(BlogImage, BlogImageAdmin)