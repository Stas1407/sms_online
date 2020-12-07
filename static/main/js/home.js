var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.querySelector(".navbar").style.top = "0px";
  } else {
    document.querySelector(".navbar").style.top = "-100px";
  }
  prevScrollpos = currentScrollPos;
}