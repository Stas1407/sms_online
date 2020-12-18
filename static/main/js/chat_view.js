
jQuery(document).ready(function(){
  cookie = Cookies.get('same_site');
  if(cookie != 'true'){
    $('.chat_icons').addClass('animation_chat_icons')
  } else {
    $('.chat_icons').css('opacity', '1')
    Cookies.remove('same_site')
  }
});

$('#message_in').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      $('#send_bt').trigger('click');  
      // $('#send_bt').addClass('clicked');

      // setTimeout(function(){
      //   $('#send_bt').removeClass('clicked');
      // }, 200);
    }
});

$('#send_bt').click(function(){
  $('#send_bt').addClass('clicked');

  setTimeout(function(){
    $('#send_bt').removeClass('clicked');
  }, 200);
})
 
$('.redirect').click(function(){
  $('.chat_view').addClass('animation_hide_on_right')
  $('.input_box').addClass('animation_hide_on_right')
  $("#"+this.id).prependTo('.top');
  Cookies.set('same_site', 'true');
  setTimeout(function(){
    window.location.href = '/chat_view';
    // window.location.href = '/chat_view' + this.id
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

  onUp(callback) {
      this.onUp = callback;

      return this;
  }

  onDown(callback) {
      this.onDown = callback;

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
      } else {
          if ( this.yDiff > 0 ) {
              this.onUp();
          } else {
              this.onDown();
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