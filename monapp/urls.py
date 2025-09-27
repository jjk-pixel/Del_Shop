from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('ajouter/', views.ajouter_produit_personnalise, name='ajouter_produit_personnalise'),
    path('produits/', views.liste_produits, name='liste_produits'),
    path('produit/<int:produit_id>/', views.detail_produit, name='detail_produit'),
    path('produit/<int:produit_id>/supprimer/', views.supprimer_produit, name='supprimer_produit'),
    path('recherche/', views.recherche, name='recherche'),    
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),
    path('categorie/<int:categorie_id>/', views.produits_par_categorie, name='produits_par_categorie'),
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-produits/', views.admin_produits, name='admin_produits'),
    path("admin-change-credentials/", views.admin_change_credentials, name="admin-change-credentials"),
]