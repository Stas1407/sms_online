jQuery(document).ready(function(){
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
});

$('.navbar-toggler').click(function(){
    $('#wrap').toggle(200);
});

$('.column').click(function(){
  $('#main_content').addClass('hide_left');
  $('nav').addClass('hide_up');
  setTimeout(function(){
    window.location.href = "/home";
  }, 600)
})
