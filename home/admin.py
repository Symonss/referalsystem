from django.contrib import admin
from home.models import Prospect, Item, Message, User

admin.site.register(Item)
admin.site.register(Message)


class ProspectAdmin(admin.ModelAdmin):
    list_display = ('agent', 'full_name', 'phone', 'status')
    list_filter = ('status', 'agent')
    search_fields = ('full_name',)
    raw_id_fields = ('agent',)


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(User)
