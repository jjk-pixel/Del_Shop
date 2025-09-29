from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from .models import Produit, ImageProduit,Categorie
from django.contrib.auth import authenticate,login
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test , login_required,login_required
from django.http import HttpResponse

# Create your views here.
def accueil(request):
    return render(request, 'index.html')

def liste_produits(request):
    categories = [
        {'cat': 'anime', 'img': 'Winner-img/Anime.jpg', 'label': 'Anime'},
        {'cat': 'transparent', 'img': 'Winner-img/Transparent.jpg', 'label': 'Transparent'},
        {'cat': 'single', 'img': 'Winner-img/Couleur.jpg', 'label': 'Single Color'},
        {'cat': 'drawing', 'img': 'Winner-img/Dessin.jpg', 'label': 'Drawing'},
    ]

    active_categorie = request.GET.get('categorie', '')

    # Filtrage des produits
    if active_categorie:
        produits = Produit.objects.filter(categorie__nom=active_categorie)
    else:
        produits = Produit.objects.all()

    # Sélection dynamique du template de base selon le thème
    theme = request.session.get("theme", "light")  # "light" par défaut
    base_template = "base_sombre.html" if theme == "dark" else "base.html"

    context = {
        'produits': produits,
        'categories': categories,
        'active_categorie': active_categorie,
        'base_template': base_template,
        'theme': theme,
    }

    return render(request, 'liste_produits.html', context)




def ajouter_produit_personnalise(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        categorie_nom = request.POST.get("categorie")

        # récupérer l'objet Categorie correspondant
        try:
            categorie_obj = Categorie.objects.get(nom=categorie_nom)
        except Categorie.DoesNotExist:
            # gérer le cas où la catégorie n'existe pas
            return HttpResponse("Cette catégorie n'existe pas", status=400)

        # créer le produit sans prix
        produit = Produit.objects.create(
            nom=nom,
            categorie=categorie_obj  # ✅ instance et non string
        )

        # gérer les images si besoin
        if request.FILES.getlist("images"):
            for image in request.FILES.getlist("images"):
                produit.images.create(image=image)

        return redirect("ajouter_produit_personnalise")  # ou où tu veux

    return render(request, "Ajouter.html")




def detail_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    # Récupérer les images du produit
    images = produit.images.all()  # assuming tu as une relation related_name='images'

    # Produits de la même catégorie sauf le produit actuel
    produits_suggestions = Produit.objects.filter(
        categorie=produit.categorie
    ).exclude(id=produit.id)[:8]  # Limite à 8 suggestions

    context = {
        'produit': produit,
        'images': images,
        'produits_suggestions': produits_suggestions,
    }
    return render(request, 'detail_produit.html', context)


def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    produit.delete()
    return redirect('admin_produits') 

def recherche(request):
    query = request.GET.get('q', '')
    produits = Produit.objects.filter(nom__icontains=query) if query else []
    return render(request, 'recherche.html', {'produits': produits, 'query': query})

def toggle_theme(request):
    current_theme = request.session.get("theme", "light")
    request.session["theme"] = "dark" if current_theme == "light" else "light"
    return redirect(request.META.get("HTTP_REFERER", "/"))


def produits_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    produits = Produit.objects.filter(categorie=categorie)
    return render(request, "liste_produits.html", {
        "produits": produits,
        "categorie": categorie
    })

def admin_required(user):
    return user.is_superuser


@login_required(login_url='admin-login')
@user_passes_test(admin_required,login_url='admin-login')
def admin_produits(request):
    produits = Produit.objects.all()
    return render(request, 'admin_produits.html', {'produits': produits})


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # seulement admin
            login(request, user)
            return redirect('admin_produits')  # page admin
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    return render(request, 'admin_login.html')

@csrf_protect  # ✅ protège la vue
@login_required(login_url='admin-login')  # 🔐 accès réservé
@user_passes_test(lambda u: u.is_staff)  # ✅ Seul un admin peut accéder
def admin_change_credentials(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user.username = username
            user.set_password(password)  # ✅ sécurité Django
            user.save()
            messages.success(request, "Identifiants mis à jour ✅. Veuillez vous reconnecter.")
            return redirect('admin-login')  # redirige vers login
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    # ✅ très important : on renvoie bien `request`
    return render(request, 'change_credentials.html', {'user': user})

