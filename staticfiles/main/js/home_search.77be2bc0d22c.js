$('.profile_img').click(function(){
    var id = $(this).parent().attr('id')
  
    $('#main_content').addClass('hide_left');
    $('nav').addClass('hide_up');
  
    setTimeout(function(){
        window.location.href = "/new_conversation/"+id
    }, 600)
})
  
$('.text').click(function(){
    var id = $(this).parent().attr('id')
  
    $('#main_content').addClass('hide_left');
    $('nav').addClass('hide_up');
  
    setTimeout(function(){
        window.location.href = "/new_conversation/"+id
    }, 600)
})

$('.icon_wrapper').click(function(){
    var id = $(this).parent().attr('id')
  
    $('#main_content').addClass('hide_left');
    $('nav').addClass('hide_up');
  
    setTimeout(function(){
        window.location.href = "/new_conversation/"+id
    }, 600)
})