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

    setTimeout(function(){
      $('.alert').slideUp(500)
    }, 1500)

    $('#form').attr("action", window.location.href)
  }); 

var ids = []

 
$('.add_person').click(function(){
    if($('#' + this.id).hasClass('clicked')){
      $('#' + this.id).removeClass('clicked')
      ids.splice(ids.indexOf(this.id), 1)
    } else {
      $('#' + this.id).addClass('clicked');
      ids.push(this.id)
    }
})

$('#next').click(function(){
  $('#next').removeClass('not_clicked');
  $('#next').addClass('next_clicked');
  $('#main_content').addClass('hide_left');
  document.querySelector(".navbar").style.top = "-100px";
})

var count = 0
var tmp_wrap = 0
$('#form').submit(function(e){
  if(count == 0){
    e.preventDefault();
  }
  if(Cookies.get('ids') && tmp_wrap == 0){
    var ids2 = Cookies.get('ids')
    ids2 = JSON.parse(ids2)
    ids = [...ids, ...ids2]
    Cookies.remove('ids')
  }
  $('#ids').val(ids.join())
  console.log(ids)
  count+=1
  setTimeout(function(){
    $('#form').submit()
  }, 500)
})

$('#search').focus(function(){
  console.log('test')
  if(Cookies.get('ids') && tmp_wrap == 0){
    var ids2 = Cookies.get('ids')
    ids2 = JSON.parse(ids2)
    ids = [...ids, ...ids2]
    tmp_wrap += 1
  }
  Cookies.set("ids", JSON.stringify(ids))
  console.log(JSON.parse(Cookies.get("ids")))
})

$('.plus_icon').click(function(){
  $('.plus_icon').addClass('plus_clicked')
  $('#search').trigger('focus')
})

$('#search').focusout(function(){
  $('.plus_icon').removeClass('plus_clicked')
})


var fileTypes = ['jpg', 'png', 'jpeg']
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