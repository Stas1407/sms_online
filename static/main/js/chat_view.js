$('#send_bt').click(function(){
  $('#send_bt').addClass('clicked');

  setTimeout(function(){
    $('#send_bt').removeClass('clicked');
  }, 200);
})
