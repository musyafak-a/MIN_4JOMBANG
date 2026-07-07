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
  var originalSlides = document.querySelectorAll("[data-slide]");
  var dotsWrap = document.getElementById("heroDots");
  var prevBtn = document.getElementById("heroPrev");
  var nextBtn = document.getElementById("heroNext");
  var track = document.getElementById("heroTrack");
  
  if (!originalSlides.length || !track) return;

  var current = 0;
  var timer = null;
  var isAnimating = false;
  var slideCount = originalSlides.length;

  originalSlides.forEach(function (_, i) {
    var dot = document.createElement("button");
    if (i === 0) dot.classList.add("is-active");
    dot.setAttribute("aria-label", "Ke slide " + (i + 1));
    dot.addEventListener("click", function () { 
      if (isAnimating) return;
      // We pass the target slide index relative to actual slides
      // Since track index is i + 1, we just do goTo(i)
      var step = i - current;
      if (step === 0) return;
      goTo(current + step);
      stopAuto(); startAuto();
    });
    dotsWrap.appendChild(dot);
  });

  var firstClone = originalSlides[0].cloneNode(true);
  var lastClone = originalSlides[slideCount - 1].cloneNode(true);
  
  firstClone.classList.add('is-clone');
  lastClone.classList.add('is-clone');
  
  track.appendChild(firstClone);
  track.insertBefore(lastClone, originalSlides[0]);

  var trackIndex = 1; 

  track.style.transition = "none";
  track.style.transform = "translateX(-100%)";

  function updateDots() {
    if(dotsWrap) {
      for(var i=0; i<dotsWrap.children.length; i++) {
        dotsWrap.children[i].classList.remove("is-active");
      }
      if (dotsWrap.children[current]) {
        dotsWrap.children[current].classList.add("is-active");
      }
    }
    
    originalSlides.forEach(function(s) { s.classList.remove("is-active"); });
    if (originalSlides[current]) {
      originalSlides[current].classList.add("is-active");
    }
  }

  function goTo(index) {
    if (isAnimating) return;
    isAnimating = true;
    
    if (index < 0) {
      current = slideCount - 1;
    } else if (index >= slideCount) {
      current = 0;
    } else {
      current = index;
    }

    trackIndex = index + 1;
    track.style.transition = "transform 0.6s cubic-bezier(0.25, 1, 0.5, 1)";
    track.style.transform = "translateX(-" + (trackIndex * 100) + "%)";
    
    updateDots();
  }

  track.addEventListener('transitionend', function(e) {
    if (e.target !== track) return;
    isAnimating = false;
    
    if (trackIndex === 0) {
      track.style.transition = "none";
      trackIndex = slideCount;
      track.style.transform = "translateX(-" + (trackIndex * 100) + "%)";
    } else if (trackIndex === slideCount + 1) {
      track.style.transition = "none";
      trackIndex = 1;
      track.style.transform = "translateX(-" + (trackIndex * 100) + "%)";
    }
  });

  function next() { if(!isAnimating) goTo(trackIndex); }
  function prev() { if(!isAnimating) goTo(trackIndex - 2); }

  function startAuto() {
    timer = setInterval(next, 6000);
  }
  function stopAuto() {
    clearInterval(timer);
  }

  if (nextBtn) nextBtn.addEventListener("click", function () { next(); stopAuto(); startAuto(); });
  if (prevBtn) prevBtn.addEventListener("click", function () { prev(); stopAuto(); startAuto(); });

  if (slideCount > 1) startAuto();
});
