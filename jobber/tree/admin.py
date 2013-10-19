from django.contrib import admin

import models


class TextNodeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)

admin.site.register(models.TextNode, TextNodeAdmin)
