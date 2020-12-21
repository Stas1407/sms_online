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
  setTimeout(function(){
    document.querySelector(".navbar").style.top = "0px";
    $('#main_content').addClass('show');
  }, 300)

  setTimeout(function(){
    $('#main_content').css('opacity', '1');
    $('#main_content').removeClass('show');
  }, 500)
});

$('.navbar-toggler').click(function(){
    $('#wrap').toggle(200);
});

$('.settings').click(function(){
  $('#main_content').addClass('hide_left');
  $('nav').addClass('hide_up');
  setTimeout(function(){
    window.location.href = "/settings";
  }, 500)
})

$('#new_group').click(function(e){
  e.preventDefault();
  var target = e.target.href;
  $('#main_content').addClass('hide_left');
  $('nav').addClass('hide_up');
  setTimeout(function(){
    window.location.href = e.target.href;
  }, 600)
})


$('.column').click(function(){
  
  $('#main_content').addClass('hide_left');
  $('nav').addClass('hide_up');
  setTimeout(function(){
    window.location.href = "/chat_view";
  }, 600)
})