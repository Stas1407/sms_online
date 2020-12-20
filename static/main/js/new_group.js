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
  

  $('.add_person').click(function(){
    $('#' + this.id).toggleClass('clicked');
})