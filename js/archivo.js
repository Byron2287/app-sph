function saludar() {
    alert("Hola");
//setinterval sirve para ejecutar secuencias de funciones    
}
//setInterval(saludar,1000,3000)

//otra forma son las funciones anonimas 7 funciones flechas
//setInterval(function(){alert("Hola")},3000)

//setInterval(()=> alert("Hola"),3000)

//setTimeout se ejecuta las veces  
//como ver lo que se seleccione de una archivo
//document.getElementsByTagName("input")[0].files[0].name 

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}