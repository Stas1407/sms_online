
jQuery(document).ready(function(){
  cookie = Cookies.get('same_site');
  if(cookie != 'true'){
    $('.chat_icons').addClass('animation_chat_icons')
  } else {
    $('.chat_icons').css('opacity', '1')
    Cookies.remove('same_site')
  }

  var paragraphs = document.querySelectorAll('p')
  for(p of paragraphs){
    if(p.innerHTML == '0'){
      p.remove()
    }
  }

  if($('#is_group').val() == "true"){
    setInterval(function(){
      var previous_author = ""
      var content = {'check':'check'}

      $.ajaxSetup({
        headers: { "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val() }
      });
      $.ajax({
        url: window.location.href,
        type: 'POST',
        data: content,
        success: function(data){
          data = JSON.parse(data)
          for(message of data){
            console.log("c: "+message.author)
            console.log("p: "+previous_author)
            if(previous_author!=message.author){
              console.log('tak')
              $('.chat').append(
                '<div class="message_wrapper"> \
                  <h5 class="author float-left">'+message.author+'</h5> \
                  <div class="others_message float-left message" id="'+ message.id +'">'+ message.text +'</div> \
                </div>'
              )
            } else{
              $('.chat').append(
                '<div class="others_message float-left message" id="'+ message.id +'">'+ message.text +'</div>'
              )
            }
            previous_author = message.author
          }
          $('.chat_view').scrollTop($('.chat_view')[0].scrollHeight)
          if($('.message').length == 2){
            window.location.reload()
          }
        }
      });
    }, 5000)
  } else {
    setInterval(function(){
      console.log('checking for events')
      var content = {'check':'check'}

      $.ajaxSetup({
        headers: { "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val() }
      });
      $.ajax({
        url: window.location.href,
        type: 'POST',
        data: content,
        success: function(data){
          data = JSON.parse(data)
          console.log(data)
          for(message of data){
            $('.chat').append('<div class="others_message float-left message" id="'+message.id+'">'+message.text+'</div>')
            $('.chat_view').scrollTop($('.chat_view')[0].scrollHeight)
            if($('.message').length == 2){
              window.location.reload()
            }
          }
        }
      });
    }, 5000)
  }
}); 

$('#message_in').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      $('#send_bt').trigger('click');  

    } 
});

$('#send_bt').click(function(){
  $('#send_bt').addClass('clicked'); 

  setTimeout(function(){
    $('#send_bt').removeClass('clicked');
  }, 200);

  var message = $('#message_in').val()
  var content = {'message_text': message}

  $.ajaxSetup({
    headers: { "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val() }
  });
  $.ajax({
    url: window.location.href,
    type: 'POST',
    data: content,
    success: function(data){
      $('.chat').append('<div class="my_message float-right message" id="'+ data +'">'+message+'</div>')
      $('.chat_view').scrollTop($('.chat_view')[0].scrollHeight)
      $('#message_in').val("")
      if($('.message').length == 1){
        window.location.reload()
      }
    }
  });
  
})

var tmp = 0
var text
var id = 0
$('.chat').on("click", ".my_message",function(){
  if(tmp == 0){
    tmp = 1
    id = this.id
    $("#"+this.id).animate({left: "100%"}, 300, function(){
      $("#"+this.id).addClass('remove')
      text = $("#"+this.id).text()
      $("#"+this.id).text("")
      $("#"+this.id).prepend('<i class="fas fa-trash"></i>')
      $("#"+this.id).animate({left: "0%"}, 300)

      var timeout = setTimeout(function(){
        $("#"+this.id).animate({left: "100%"}, 300, function(){
          $("#"+this.id).removeClass('remove')
          $("#"+this.id).text(text)
          $(".fa-trash").remove()
          $("#"+this.id).animate({left: "0%"}, 300)
          tmp = 0
        })
        $('#'+this.id).unbind('mouseleave')
      }, 5000)

      $('.remove').mouseleave(function(){
        clearTimeout(timeout)
        $("#"+this.id).animate({left: "100%"}, 300, function(){
          $("#"+this.id).removeClass('remove')
          $("#"+this.id).text(text)
          $(".fa-trash").remove()
          $("#"+this.id).animate({left: "0%"}, 300)
          tmp = 0
        })
        $('#'+this.id).unbind('mouseleave')
      })

      $('.fa-trash').click(function(){
        if(confirm("Are you sure you want to delete this message")){
          var id = $('.fa-trash').parent().attr('id')
          $.ajax({
            url: "/delete_message/" + id,
            type: 'GET',
            success: function(data){
              $('#'+id).remove()
            }
          });
        }
      })
    })
  }
}) 
 
$('.redirect').click(function(){
  $('.chat_view').addClass('animation_hide_on_right')
  $('.input_box').addClass('animation_hide_on_right')
  $('.flip-card').hover(function(){
    $('.flip-card-inner').css('transform', 'none')
    $('p').css('opacity', '1')
  })
  $("#"+this.id).prependTo('.top');
  id = $(this).attr('id')
  Cookies.set('same_site', 'true');
  setTimeout(function(){
    if($('#'+id).hasClass('group_redirect')){
      window.location.href = '/group/' + id.split('i')[1].replace('c', '').replace('g', '')
    } else {
      window.location.href = '/conversation/' + id.split('i')[1].replace('c', '').replace('g', '')
    }
  }, 300)
})

$('#back').click(function(){
  $('.chat_view').addClass('animation_hide_on_right')
  $('.input_box').addClass('animation_hide_on_right')
  $('.chat_icons').addClass('animation_hide')

  setTimeout(function(){
    window.location.href = '/home';
  }, 300)
})

$('.flip-card').click(function(){
  $('.flip-card-inner').css('transform', 'rotateY(180deg)')
  $('#top_unread').css('opacity', '0')
  setTimeout(() => {
    $('.flip-card-inner').css('transform', 'none')
    $('#top_unread').css('opacity', '1')
  }, 3000);
})

$('.settings').click(function(){
  $('.chat_view').addClass('animation_hide_on_right')
  $('.input_box').addClass('animation_hide_on_right')
  $('.chat_icons').addClass('animation_hide')

  var id = this.id.toString().split('s')[1];
  console.log(id)

  setTimeout(function(){
    window.location.href = '/settings/' + id;
  }, 300)
})

class Swipe {
  constructor(element) {
      this.xDown = null;
      this.yDown = null;
      this.element = typeof(element) === 'string' ? document.querySelector(element) : element;

      this.element.addEventListener('touchstart', function(evt) {
          this.xDown = evt.touches[0].clientX;
          this.yDown = evt.touches[0].clientY;
      }.bind(this), false);

  }

  onLeft(callback) {
      this.onLeft = callback;

      return this;
  }

  onRight(callback) {
      this.onRight = callback;

      return this;
  }

  handleTouchMove(evt) {
      if ( ! this.xDown || ! this.yDown ) {
          return;
      }

      var xUp = evt.touches[0].clientX;
      var yUp = evt.touches[0].clientY;

      this.xDiff = this.xDown - xUp;
      this.yDiff = this.yDown - yUp;

      if ( Math.abs( this.xDiff ) > Math.abs( this.yDiff ) ) { // Most significant.
          if ( this.xDiff > 0 ) {
              this.onLeft();
          } else {
              this.onRight();
          }
      } 

      // Reset values.
      this.xDown = null;
      this.yDown = null;
  }

  run() {
      this.element.addEventListener('touchmove', function(evt) {
          this.handleTouchMove(evt);
      }.bind(this), false);
  }
}

var is_shown = false;
var swiper = new Swipe('body');
swiper.onRight(function() { 
  if(!is_shown){
    $('.chat_icons').addClass('animation_show')
    
    setTimeout(function(){
      $('.chat_icons').removeClass('animation_hide')
    }, 300)
    is_shown = true;
  }
});
swiper.onLeft(function() { 
  if(is_shown){
    $('.chat_icons').addClass('animation_hide')
    
    setTimeout(function(){
      $('.chat_icons').removeClass('animation_show')
    }, 300)
  }
  is_shown = false;
});
swiper.run();

var elem = document.querySelector('.chat_view');
elem.scrollTop = elem.scrollHeight;