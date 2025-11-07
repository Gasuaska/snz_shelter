from django.contrib import admin
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse

from .models import (
    CatInfo, DogInfo, CatHealth, DogHealth, Owner, DogDescription, AnimalPhoto)


@admin.action(description="Сгенерировать PDF карточки выбранных собак")
def dog_card_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dogs.pdf"'
    for dog in queryset:
        html = render_to_string("pdf/dog_card.html", {"dog": dog})
        pisa_status = pisa.CreatePDF(html, dest=response)

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
    actions = (dog_card_pdf,)


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
admin.site.register(AnimalPhoto, AnimalPhotoAdmin)


admin.site.empty_value_display = 'Не задано'