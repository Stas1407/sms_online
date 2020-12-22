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

// var t1;
// var t2;

$('.settings_div').hover(function(){
  console.log('hover')
  $('.settings_inner_div').on("mouseover",function(){
    console.log('over')
    var id = $('#'+ this.id + '> .settings_div > img').attr('id')
    $('#' + id).addClass('settings_hover')
    
    var id2 = $('#'+ this.id + '> .remove').attr('id');
    var id3 = $('#'+ this.id + '> .settings_inner_icon').attr('id');

    // t1 = setTimeout(function(){
      $('#' + id3).addClass('settings_extended');
    // }, 100)

    // t2 = setTimeout(function(){
      $('#' + id2).addClass('remove_extended');
    // }, 400)
  })

  $('.settings_inner_div').on("mouseleave", function(){
    // window.clearTimeout(t1)
    // window.clearTimeout(t2)
    $('.settings_inner_div').unbind('mouseenter mouseleave mouseover');
    var id3 = $('#'+ this.id + '> .settings_inner_icon').attr('id')
    var id2 = $('#'+ this.id + '> .remove').attr('id')
    var id = $('#'+ this.id + '> .settings_div > img').attr('id')
    $('#' + id3).removeClass('settings_extended')
    $('#' + id2).removeClass('remove_extended')
    $('#' + id).removeClass('settings_hover')
    console.log('leave')
    // // setTimeout(function(){
    //   $('#' + id3).removeClass('settings_extended')
    // // }, 600)

    // // setTimeout(function(){
    //    $('#' + id).removeClass('settings_hover')
    // // }, 400) 
  })
}, function(){})
