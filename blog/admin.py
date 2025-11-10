from django.contrib import admin

from .models import Category, Post


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


admin.site.register(Post, PostAdmin)