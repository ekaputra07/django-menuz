from django.contrib import admin
from menuz.models import Menuz

class MenuzAdmin(admin.ModelAdmin):
    list_display = ('title','position')
    save_on_top = True

admin.site.register(Menuz, MenuzAdmin)

