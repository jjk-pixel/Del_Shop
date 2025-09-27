from django.contrib import admin
from .models import Produit, ImageProduit, Categorie
from django.utils.html import format_html
# Register your models here.

class ImageProduitInline(admin.TabularInline):
    model = ImageProduit
    extra = 1

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'image_preview')  # seuls nom et image

    inlines = [ImageProduitInline]

    def image_preview(self, obj):
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" style="height:50px;width:auto;border-radius:5px;" />',
                first_image.image.url
            )
        return "-"
    image_preview.short_description = "Image"

admin.site.register(Produit, ProduitAdmin)

admin.site.register(Categorie)

admin.site.register(ImageProduit)