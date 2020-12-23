jQuery(document).ready(function(){
    $('#edit_nick_in').hide()
    $('#nick_done').hide()

    var cw = $('#profile_pic').width();
    $('#profile_pic').css({'height':cw+'px'});   
    
    var c2 = $('#camera_icon').width();
    $('#camera_icon').css({'height':c2+'px'}); 

    var c3 = $('#switch_inner').width();
    
    $('#switch_inner').css({'height':c3+'px'}); 

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

$(window).resize(function(){
    var cw = $('#profile_pic').width();
    $('#profile_pic').css({'height':cw+'px'});    
})

$('#switch_inner').click(function(){
  $('#switch_inner').toggleClass('switch_clicked')
})

$('#done_bt').click(function(){
  $('#done_bt').addClass('done_clicked');
  $('#main_content').addClass('hide_left');
  $('nav').css('top', '-100px');
  setTimeout(function(){
    window.location.href = "/home";
  }, 500)
})

var fileTypes = ['jpg', 'jpeg', 'png'];

document.getElementById('img_input').onchange = function (evt) {
  var tgt = evt.target || window.event.srcElement,
      files = tgt.files;
  var extension = files[0].name.split('.').pop().toLowerCase(),  // todo: check ext on server side
      isSuccess = fileTypes.indexOf(extension) > -1;
  // FileReader support

  if (FileReader && files && files.length && isSuccess) {
      var fr = new FileReader();
      fr.onload = function () {
          document.getElementById('profile_pic').src = fr.result;
          
      }
      fr.readAsDataURL(files[0]);
  }
}

$('#nick_edit_icon').click(function(){
  $('#edit_nick_in').show()
  $('#nick_done').show()
  $('#nick_edit_icon').hide()
  $('#nick').hide()
})

$('#nick_done').click(function(){
  $('#edit_nick_in').hide()
  $('#nick_done').hide()
  $('#nick_edit_icon').show()
  $('#nick').show()
  $('#nick').text($('#edit_nick_in').val())
})