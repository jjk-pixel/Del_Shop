def panier_total(request):
    panier = request.session.get("panier", {})
    total = sum(item['quantite'] for item in panier.values())
    return {'panier_total': total}

def theme_context(request):
    theme = request.session.get("theme", "light")
    base_template = "base_sombre.html" if theme == "dark" else "base.html"
    return {"base_template": base_template}
