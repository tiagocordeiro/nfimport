from django.contrib import admin

from .models import Product, Nota, NotaItens


class ProductAdmin(admin.ModelAdmin):
    list_display = ('maquina_pt',)


class NotaItensInline(admin.StackedInline):
    model = NotaItens
    extra = 0


class NotaAdmin(admin.ModelAdmin):
    list_display = ('description',)
    inlines = [
        NotaItensInline,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Nota, NotaAdmin)
