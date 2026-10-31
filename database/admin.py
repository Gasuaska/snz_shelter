from django import forms
from django.contrib import admin
from django.http import HttpResponse
from taggit.admin import Tag
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, admin
from django.http import HttpResponse
from django.db.models import Exists, OuterRef
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import AnimalTag
from .forms import MultipleFileField
from cats.models import CatInfo, CatDescription, CatPhoto, CatHealth
from dogs.models import DogInfo, DogDescription, DogPhoto, DogHealth
from .pdf_utils import arrange_four_per_a4
from .utils import prepare_dog_card


class DogWithoutMainPhotoFilter(admin.SimpleListFilter):
    title = 'главное фото собаки'
    parameter_name = 'dog_without_main'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Не назначено'),
        )

    def queryset(self, request, queryset):
        if self.value() != 'yes':
            return queryset

        main_photos = DogPhoto.objects.filter(
            animal_id=OuterRef('animal_id'),
            is_main=True,
        )

        return queryset.alias(
            has_main=Exists(main_photos)
        ).filter(has_main=False)

@admin.action(description='Опубликовать выбранные фото в галерее')
def publish_in_gallery(modeladmin, request, queryset):
    updated = queryset.update(show_in_gallery=True)
    modeladmin.message_user(
        request,
        f'Опубликовано фотографий: {updated}'
    )


@admin.action(description='Убрать выбранные фото из галереи')
def unpublish_from_gallery(modeladmin, request, queryset):
    updated = queryset.update(show_in_gallery=False)
    modeladmin.message_user(
        request,
        f'Снято с публикации фотографий: {updated}'
    )

@admin.action(description='Скачать карточки для вольеров (4 на A4)')
def download_dog_cards(modeladmin, request, queryset):
    cards = [
        prepare_dog_card(dog)
        for dog in queryset
    ]

    html = render_to_string(
        'pdf/dog_cards.html',
        {'cards': cards},
        request=request,
    )

    a6_pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri('/'),
    ).write_pdf()

    a4_pdf = arrange_four_per_a4(a6_pdf)

    response = HttpResponse(
        a4_pdf,
        content_type='application/pdf',
    )

    response['Content-Disposition'] = (
        'attachment; filename="dog_cards_A4.pdf"'
    )

    return response


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            if len(data) > 10:
                raise forms.ValidationError('Можно загрузить не больше 10 фотографий за раз.')
            return [single_clean(item, initial) for item in data]
        return [single_clean(data, initial)]


class MultipleDogPhotoForm(forms.Form):
    images = MultipleFileField(
        label='Фотографии',
        required=False,
    )

class DogInfoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=AnimalTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = DogInfo
        fields = '__all__'

    class Media:
            css = {
                'all': ('admin/custom_checkboxes.css',)
            }

class DogPhotoInline(admin.TabularInline):
    model = DogPhoto
    extra = 0
    readonly_fields = ('photo_preview',)
    fields = ('photo_preview', 'image', 'is_main')

    @admin.display(description='Предпросмотр')
    def photo_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height: 110px; '
                'width: 150px; object-fit: contain; '
                'border-radius: 5px;">',
                obj.thumbnail.url
            )
        return '—'


class CatPhotoInline(admin.TabularInline):
    model = CatPhoto
    extra = 0
    readonly_fields = ('photo_preview',)
    fields = ('photo_preview', 'image', 'is_main')

    @admin.display(description='Предпросмотр')
    def photo_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height: 110px; '
                'width: 150px; object-fit: contain; '
                'border-radius: 5px;">',
                obj.thumbnail.url
            )
        return '—'


class CatInfoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=AnimalTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CatInfo
        fields = '__all__'
        
    class Media:
            css = {
                'all': ('admin/custom_checkboxes.css',)
            }


class PetInfoAdmin(admin.ModelAdmin):
    list_editable = (
        'gender', 'birth_date',
        'intake_date', 'is_at_shelter')
    list_display = (
        'name', 'gender', 'birth_date',
        'intake_date', 'is_at_shelter', 'get_tags')
    search_fields = ('name', 'get_tags')
    list_filter = (
        'gender', 'birth_date', 'intake_date', 'is_at_shelter', 'is_neutered')
    list_display_links = ('name',)

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    get_tags.short_description = 'Теги'


class DogHealthInline(admin.StackedInline):
    model = DogHealth
    extra = 0

class DogDescriptionInline(admin.StackedInline):
    model = DogDescription
    extra = 0

class CatDescriptionInline(admin.StackedInline):
    model = CatDescription
    extra = 0

class CatHealthInline(admin.StackedInline):
    model = CatHealth
    extra = 0


class DogInfoAdmin(PetInfoAdmin):
    form = DogInfoForm
    inlines = (DogHealthInline, DogPhotoInline, DogDescriptionInline)
    list_display = ('name', 'gender', 'birth_date', 'weight',
                    'intake_date', 'is_at_shelter', 'priority', 'urgent')
    list_editable = ('gender', 'birth_date', 'weight', 'intake_date', 'is_at_shelter',
                     'priority', 'urgent')
    search_fields = ('name', 'tags__name')
    list_filter = ('gender', 'birth_date', 'intake_date',
                   'is_at_shelter', 'is_neutered', 'priority', 'urgent')
    list_display_links = ('name',)

    def get_tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Теги'

    actions = [download_dog_cards]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/upload-photos/',
                self.admin_site.admin_view(self.upload_photos),
                name='dogs_doginfo_upload_photos',
            ),
        ]
        return custom_urls + urls

    def upload_photos(self, request, object_id):
        dog = get_object_or_404(DogInfo, pk=object_id)

        if not self.has_change_permission(request, dog):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        if request.method == 'POST':
            form = MultipleDogPhotoForm(request.POST, request.FILES)

            if form.is_valid():
                images = form.cleaned_data['images']

                for image in images:
                    DogPhoto.objects.create(
                        animal=dog,
                        image=image,
                    )

                messages.success(
                    request,
                    f'Загружено фотографий: {len(images)}'
                )

                return redirect(
                    reverse('admin:dogs_doginfo_change', args=[dog.pk])
                )
        else:
            form = MultipleDogPhotoForm()

        context = {
            **self.admin_site.each_context(request),
            'title': f'Загрузка фотографий: {dog.name}',
            'form': form,
            'dog': dog,
            'opts': self.model._meta,
        }

        return render(
            request,
            'admin/dogs/upload_photos.html',
            context,
        )


class CatInfoAdmin(PetInfoAdmin):
    form = CatInfoForm
    list_display = ('name', 'gender', 'birth_date', 'weight',
                    'intake_date', 'is_at_shelter', 'get_tags')
    list_editable = ('gender', 'birth_date', 'weight', 'intake_date', 'is_at_shelter')
    search_fields = ('name', 'tags__name')
    list_filter = ('gender', 'birth_date',
                   'intake_date', 'is_at_shelter', 'is_neutered')
    list_display_links = ('name',)
    inlines = (CatHealthInline, CatPhotoInline, CatDescriptionInline)

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Теги'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/upload-photos/',
                self.admin_site.admin_view(self.upload_photos),
                name='cats_catinfo_upload_photos',
            ),
        ]
        return custom_urls + urls

    def upload_photos(self, request, object_id):
        cat = get_object_or_404(CatInfo, pk=object_id)

        if not self.has_change_permission(request, cat):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        if request.method == 'POST':
            form = MultipleDogPhotoForm(request.POST, request.FILES)

            if form.is_valid():
                images = form.cleaned_data['images']

                for image in images:
                    CatPhoto.objects.create(
                        animal=cat,
                        image=image,
                    )

                messages.success(
                    request,
                    f'Загружено фотографий: {len(images)}'
                )

                return redirect(
                    reverse('admin:cats_catinfo_change', args=[cat.pk])
                )
        else:
            form = MultipleDogPhotoForm()

        context = {
            **self.admin_site.each_context(request),
            'title': f'Загрузка фотографий: {cat.name}',
            'form': form,
            'cat': cat,
            'opts': self.model._meta,
        }

        return render(
            request,
            'admin/cats/upload_photos.html',
            context,
        )

class DogDescriptionAdmin(admin.ModelAdmin):
    list_display = ('dog_name',)
    search_fields = ('dog__name',)
    def dog_name(self, obj):
        if obj.dog:
            return obj.dog.name
        return '—'

    dog_name.short_description = 'Имя собаки'


class CatDescriptionAdmin(admin.ModelAdmin):
    list_display = ('cat_name',)
    search_fields = ('cat__name',)
    def cat_name(self, obj):
        if obj.cat:
            return obj.cat.name
        return '—'

    cat_name.short_description = 'Имя кошки'


class AnimalPhotoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['animal']
    list_display = ('animal__name', 'animal', 'is_main', 'show_in_gallery', 'image', 'image_preview')
    list_editable = ('animal', 'is_main', 'show_in_gallery')
    search_fields = ('animal__name',)
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

class DogPhotoAdmin(AnimalPhotoAdmin):
    list_filter = (DogWithoutMainPhotoFilter,)
    
class AnimalTagAmdin(admin.ModelAdmin):
    search_fields = ('name', 'description')


admin.site.register(CatInfo, CatInfoAdmin)
admin.site.register(DogInfo, DogInfoAdmin)
admin.site.register(CatHealth)
admin.site.register(DogHealth)
admin.site.register(DogDescription, DogDescriptionAdmin)
admin.site.register(CatDescription, CatDescriptionAdmin)
admin.site.register(DogPhoto, DogPhotoAdmin)
admin.site.register(CatPhoto, AnimalPhotoAdmin)
admin.site.register(AnimalTag, AnimalTagAmdin)
admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Tag)
admin.site.site_header = 'Друг из приюта'
admin.site.site_title = 'Управление приютом'
admin.site.index_title = 'Панель управления'