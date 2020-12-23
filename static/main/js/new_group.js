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

$('#next').click(function(){
  $('#next').removeClass('not_clicked');
  $('#next').addClass('next_clicked');
  $('#main_content').addClass('hide_left');
  document.querySelector(".navbar").style.top = "-100px";

  setTimeout(function(){
    window.location.href = '/chat_view';
  }, 600)
})

document.getElementById('file_input').onchange = function (evt) {
  var tgt = evt.target || window.event.srcElement,
      files = tgt.files;

  var extension = files[0].name.split('.').pop().toLowerCase(),  // todo: check ext on server side
      isSuccess = fileTypes.indexOf(extension) > -1;

  // FileReader support
  if (FileReader && files && files.length && isSuccess) {
      var fr = new FileReader();
      fr.onload = function () {
          document.getElementById('group_icon').src = fr.result;
          $('#group_icon').addClass('group_icon_new')
      }
      fr.readAsDataURL(files[0]);
  }
}