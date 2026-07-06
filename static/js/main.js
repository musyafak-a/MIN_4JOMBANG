document.addEventListener("DOMContentLoaded", function () {
  /* ---------- Mobile nav toggle ---------- */
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("navMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var isOpen = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen);
    });
  }

  /* ---------- Hero carousel ---------- */
  var slides = document.querySelectorAll("[data-slide]");
  var dotsWrap = document.getElementById("heroDots");
  var prevBtn = document.getElementById("heroPrev");
  var nextBtn = document.getElementById("heroNext");
  if (!slides.length) return;

  var current = 0;
  var timer = null;

  slides.forEach(function (_, i) {
    var dot = document.createElement("button");
    if (i === 0) dot.classList.add("is-active");
    dot.setAttribute("aria-label", "Ke slide " + (i + 1));
    dot.addEventListener("click", function () { goTo(i); });
    dotsWrap.appendChild(dot);
  });

  var track = document.getElementById("heroTrack");

  function goTo(index) {
    slides[current].classList.remove("is-active");
    if(dotsWrap && dotsWrap.children[current]) {
      dotsWrap.children[current].classList.remove("is-active");
    }
    
    current = (index + slides.length) % slides.length;
    
    if(track) {
      track.style.transform = "translateX(-" + (current * 100) + "%)";
    }
    
    slides[current].classList.add("is-active");
    if(dotsWrap && dotsWrap.children[current]) {
      dotsWrap.children[current].classList.add("is-active");
    }
  }


  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  function startAuto() {
    timer = setInterval(next, 6000);
  }
  function stopAuto() {
    clearInterval(timer);
  }

  if (nextBtn) nextBtn.addEventListener("click", function () { next(); stopAuto(); startAuto(); });
  if (prevBtn) prevBtn.addEventListener("click", function () { prev(); stopAuto(); startAuto(); });

  if (slides.length > 1) startAuto();
});
