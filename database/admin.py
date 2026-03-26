from django import forms
from django.contrib import admin
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import HttpResponse
from taggit.admin import Tag
from django.utils.html import format_html

from .models import Owner, AnimalTag
from cats.models import CatInfo, CatDescription, CatPhoto, CatHealth
from dogs.models import DogInfo, DogDescription, DogPhoto, DogHealth
from .generate_cards import draw_card


# @admin.action(description="Сгенерировать PDF карточки выбранных собак")
# def generate_pdf(modeladmin, request, queryset):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="dogs_cards.pdf"'

#     c = canvas.Canvas(response, pagesize=A4)
#     page_w, page_h = A4
#     margin = 15 * mm
#     gap = 8 * mm
#     card_w = (page_w - 2 * margin - gap) / 2.0
#     card_h = (page_h - 2 * margin - gap) / 2.0

#     positions = []
#     for row in range(2):
#         for col in range(2):
#             x = margin + col * (card_w + gap)
#             y = page_h - margin - (row + 1) * card_h - row * gap
#             positions.append((x, y))

#     idx = 0
#     for dog in queryset:
#         x, y = positions[idx % 4]
#         draw_card(c, x, y, card_w, card_h, dog)
#         idx += 1
#         if idx % 4 == 0:
#             c.showPage()
#     if idx % 4 != 0:
#         c.showPage()

#     c.save()
#     return response


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


class CatHealthInline(admin.StackedInline):
    model = CatHealth
    extra = 0


class DogInfoAdmin(PetInfoAdmin):
    form = DogInfoForm
    inlines = (DogHealthInline,)
    list_display = ('name', 'gender', 'birth_date',
                    'intake_date', 'is_at_shelter', 'priority', 'urgent')
    list_editable = ('gender', 'birth_date', 'intake_date', 'is_at_shelter',
                     'priority', 'urgent')
    search_fields = ('name', 'tags__name')
    list_filter = ('gender', 'birth_date', 'intake_date',
                   'is_at_shelter', 'is_neutered', 'priority', 'urgent')
    list_display_links = ('name',)

    def get_tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Теги'


class CatInfoAdmin(PetInfoAdmin):
    form = CatInfoForm
    list_display = ('name', 'gender', 'birth_date',
                    'intake_date', 'is_at_shelter', 'get_tags')
    list_editable = ('gender', 'birth_date', 'intake_date', 'is_at_shelter')
    search_fields = ('name', 'tags__name')
    list_filter = ('gender', 'birth_date',
                   'intake_date', 'is_at_shelter', 'is_neutered')
    list_display_links = ('name',)
    inlines = (CatHealthInline,)

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Теги'


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
    list_display = ('animal_name', 'image', 'image_preview')
    search_fields = ('animal__name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px; max-width:150px;" />', 
                obj.image.url)
        return '-'

    def animal_name(self, obj):
        if obj.animal:
            return obj.animal.name
        return '—'


class AnimalTagAmdin(admin.ModelAdmin):
    search_fields = ('name', 'description')

admin.site.register(CatInfo, CatInfoAdmin)
admin.site.register(DogInfo, DogInfoAdmin)
admin.site.register(CatHealth)
admin.site.register(DogHealth)
admin.site.register(Owner)
admin.site.register(DogDescription, DogDescriptionAdmin)
admin.site.register(CatDescription, CatDescriptionAdmin)
admin.site.register(DogPhoto, AnimalPhotoAdmin)
admin.site.register(CatPhoto, AnimalPhotoAdmin)
admin.site.register(AnimalTag, AnimalTagAmdin)
admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Tag)