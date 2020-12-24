jQuery(document).ready(function(){
    $('#edit_nick_in').hide()
    $('#nick_done').hide()

    $('#old_passwd_done_icon').hide()
    $('#new_passwd_done_icon').hide()

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


//-------------------- Edit nick ----------------------------
// Start editing
$('#nick_edit_icon').click(function(){
  $('#edit_nick_in').show()
  $('#nick_done').show()
  $('#nick_edit_icon').hide()
  $('#nick').hide()
})

// Save and exit editing
$('#nick_done').click(function(){
  $('#edit_nick_in').hide()
  $('#nick_done').hide()
  $('#nick_edit_icon').show()
  $('#nick').show()
  $('#nick').text($('#edit_nick_in').val())
})
//-----------------------------------------------------------


//-------------------- Edit password ------------------------
var stage = 0
var current_bt;
var old_password;
var new_password;

$('#passwd_edit_icon').click(function(){
  $('#passwd_in').focus()
})

// Start editing password - Type in old password (click on input)
$('#passwd_in').focus(function(){
  if(stage == 0){
    // Hide label
    $('#passwd_label').animate({opacity: '0'})

    // Wait until label hides and change text
    setTimeout(function(){
      $('#passwd_label').text('Type in your current password')
    }, 400)

    setTimeout(function(){
      $('#passwd_label').animate({opacity: '100%'})   // Show label
      $('#passwd_in').val('')                         // Reset input value
      $('#old_passwd_done_icon').show(300)            // Show a new icon
      current_bt = $('#old_passwd_done_icon')
      $('#passwd_edit_icon').hide(300)                // Hide edit icon
    }, 500)

    stage = 1   // Prevent executing twice
  }
})

// Type in a new password (save and check old password)
$('#old_passwd_done_icon').click(function(){
  // Hide label
  $('#passwd_label').animate({opacity: '0'})

  // Wait until label hides and change text
  setTimeout(function(){
    $('#passwd_label').text('Type in a new password')
  }, 400)

  old_password = $('#passwd_in').val()    // Save an old password

  var correct = true
  // -------------- Check if old password is correct ------------

  // -----------------------------------------------------------
  if(!correct){
    // Wait until label hides and change text
    setTimeout(function(){
      $('#passwd_label').text('Wrong password')
    }, 400)

    setTimeout(function(){
      $('#passwd_label').animate({opacity: '100%'})   // Show label

      // Return to starting point
      $('#old_passwd_done_icon').hide(300)
      $('#passwd_edit_icon').show(300)
      current_bt = $('#passwd_edit_icon')
      stage = 0;
    }, 500)

    setTimeout(function(){
      $('#passwd_label').text('Password')
    }, 2000)

  } else {
    setTimeout(function(){
      $('#passwd_label').animate({opacity: '100%'})   // Show label
      $('#old_passwd_done_icon').hide(300)            // Hide old icon
      $('#new_passwd_done_icon').show(300)            // Show new icon (To trigger next stage)
      current_bt = $('#new_passwd_done_icon')
      $('#passwd_in').val('')                         // Reset input value
    }, 500)
  }
})


// Done - Save new password
$('#new_passwd_done_icon').click(function(){
  // Hide label
  $('#passwd_label').animate({opacity: '0'})
  
  // Wait until label hides and change text
  setTimeout(function(){
    $('#passwd_label').text('Done')
  }, 400)

  new_password = $('#passwd_in').val()

  if(new_password.length < 8){
    // Wait until label hides and change text
    setTimeout(function(){
      $('#passwd_label').text('Password is too short')
    }, 400)

    setTimeout(function(){
      $('#passwd_label').animate({opacity: '100%'})   // Show label
    }, 500)

    setTimeout(function(){
      $('#passwd_label').text('Type in a new password')
    }, 2000)
  } else {

    // Show label, change input value not to contain password
    setTimeout(function(){
      $('#passwd_label').animate({opacity: '100%'})
      $('#passwd_in').val('**************')
    }, 500)

    // Hide label again
    setTimeout(function(){
      $('#passwd_label').animate({opacity: '0'})
    }, 1500)
    
    // Reset label text to the starting one
    setTimeout(function(){
      $('#passwd_label').text('Password')
    }, 2000)

    // Reset input state to the starting one
    setTimeout(function(){
      $('#passwd_label').animate({opacity: '100%'})
      $('#new_passwd_done_icon').hide(300)
      $('#passwd_edit_icon').show(300)
      current_bt = $('#passwd_edit_icon')
    }, 2500)
    
    stage = 0;  // Go back to beginning
  }
})

// Check if enter was clicked and trigger a button click
// to go to the next stage
$('#passwd_in').keypress(function(event){
  var keycode = (event.keyCode ? event.keyCode : event.which);
  if(keycode == '13'){
    current_bt.click()
  }
})

//---------------------------------------------------------