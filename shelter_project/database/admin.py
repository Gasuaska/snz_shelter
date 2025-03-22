from django.contrib import admin

from .models import CatInfo, DogInfo, CatHealth, DogHealth, Owner


admin.site.register(CatInfo)
admin.site.register(DogInfo)
admin.site.register(CatHealth)
admin.site.register(DogHealth)
admin.site.register(Owner)
