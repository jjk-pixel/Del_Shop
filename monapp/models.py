from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    description = models.TextField(blank=True, null=True)
    image_principale = models.ImageField(upload_to="produits/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/')

    def __str__(self):
        return f"Image de {self.produit.nom}"
