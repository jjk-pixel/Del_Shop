
function updateShoeColor(event) {
    const shoeImage = document.getElementById('shoe-image');
    if (event.target.name === 'couleur') {
      const color = event.target.value;

      if (color === 'red') {
        shoeImage.style.filter = 'hue-rotate(0deg) saturate(150%)'; // rouge
      } else if (color === 'blue') {
        shoeImage.style.filter = 'hue-rotate(190deg) saturate(150%)'; // bleu
      } else {
        shoeImage.style.filter = 'none'; // noir (original)
      }
    }
  }
   function rechercher() {
    const valeur = document.getElementById("searchInput").value;
    if (valeur.trim() !== "") {
      window.location.href = `recherche.html?q=${encodeURIComponent(valeur)}`;
    } else {
      alert("Veuillez entrer un mot-clé !");
    }
  }
const toggleButton = document.getElementById('toggle-theme');

// Vérifiez le thème actuel dans le stockage local
const currentTheme = localStorage.getItem('theme') || 'light';
if (currentTheme === 'dark') {
    document.body.classList.add('dark');
}

toggleButton.addEventListener('click', () => {
    console.log('Bouton cliqué'); // Ajoutez ceci pour vérifier si l'événement fonctionne
    document.body.classList.toggle('dark');
    const newTheme = document.body.classList.contains('dark') ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);
});

