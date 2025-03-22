from django.contrib import admin

from .models import CatInfo, DogInfo, CatHealth, DogHealth, Owner


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


class CatInfoAdmin(PetInfoAdmin):
    pass


admin.site.register(CatInfo, CatInfoAdmin)
admin.site.register(DogInfo, DogInfoAdmin)
admin.site.register(CatHealth)
admin.site.register(DogHealth)
admin.site.register(Owner)

admin.site.empty_value_display = 'Не задано'
