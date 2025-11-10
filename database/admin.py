from django.contrib import admin
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse

from .models import (
    CatInfo, DogInfo, CatHealth, DogHealth, Owner, DogDescription,
    DogPhoto, CatPhoto, CatDescription)
from .generate_cards import draw_card


@admin.action(description="Сгенерировать PDF карточки выбранных собак")
def generate_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dogs_cards.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    page_w, page_h = A4
    margin = 15 * mm
    gap = 8 * mm
    card_w = (page_w - 2 * margin - gap) / 2.0
    card_h = (page_h - 2 * margin - gap) / 2.0

    positions = []
    for row in range(2):
        for col in range(2):
            x = margin + col * (card_w + gap)
            y = page_h - margin - (row + 1) * card_h - row * gap
            positions.append((x, y))

    idx = 0
    for dog in queryset:
        x, y = positions[idx % 4]
        draw_card(c, x, y, card_w, card_h, dog)
        idx += 1
        if idx % 4 == 0:
            c.showPage()
    if idx % 4 != 0:
        c.showPage()

    c.save()
    return response


class PetInfoAdmin(admin.ModelAdmin):
    list_editable = (
        'gender', 'birth_date', 'intake_date', 'is_at_shelter')
    list_display = (
        'name', 'gender', 'birth_date', 'intake_date', 'is_at_shelter')
    search_fields = ('name',)
    list_filter = (
        'gender', 'birth_date', 'intake_date', 'is_at_shelter', 'is_neutered')
    list_display_links = ('name',)


class DogHealthInline(admin.StackedInline):
    model = DogHealth
    extra = 0


class DogInfoAdmin(PetInfoAdmin):
    inlines = (
        DogHealthInline,
    )
    actions = (generate_pdf,)


class CatInfoAdmin(PetInfoAdmin):
    pass

class AnimalPhotoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['animal']

admin.site.register(CatInfo, CatInfoAdmin)
admin.site.register(DogInfo, DogInfoAdmin)
admin.site.register(CatHealth)
admin.site.register(DogHealth)
admin.site.register(Owner)
admin.site.register(DogDescription)
admin.site.register(CatDescription)
admin.site.register(DogPhoto, AnimalPhotoAdmin)
admin.site.register(CatPhoto, AnimalPhotoAdmin)


admin.site.empty_value_display = 'Не задано'