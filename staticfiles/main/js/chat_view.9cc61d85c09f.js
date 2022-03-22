
import Swipe from "/static/main/js/Swipe.js"

jQuery(document).ready(function(){

  // -------------- Setup socket --------
  const conversation_id = (window.location.href).substring((window.location.href).lastIndexOf('/') + 1)
  let connectionString = ""
  if($('#is_group').val() == "true"){
    connectionString = 'ws://' + window.location.host + '/ws/group/' + conversation_id + "/"
  } else {
    connectionString = 'ws://' + window.location.host + '/ws/conversation/' + conversation_id + "/"
  }
  const socket = new WebSocket(connectionString)
  // ------------------------------------

  let cookie = Cookies.get('same_site');
  if(cookie != 'true'){
    $('.chat_icons').addClass('animation_chat_icons')
  } else {
    $('.chat_icons').css('opacity', '1')
    Cookies.remove('same_site')
  }

  var paragraphs = document.querySelectorAll('p')
  for(const p of paragraphs){
    if(p.innerHTML == '0'){
      p.remove()
    }
  }

  // ------------------- Message sending ------------------
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

    const message = $('#message_in').val()
    const token = Math.random().toString(36).replace("0.", "");
    const data = {'message': message, 'action': "SEND", 'token': token}

    socket.send(JSON.stringify(data))

    $('.chat').append('<div class="my_message float-right message" id="'+ token +'">'+message+'</div>')
    $('.chat_view').scrollTop($('.chat_view')[0].scrollHeight)
    $('#message_in').val("")
    if($(".chat").children().length < 3 && $('#is_group').val() != "true"){
      window.location.reload()
    }
  })
  // ----------------------------------------------------

  // ------------------------- Message deleting -------------------
  var tmp = 0
  var text
  var id = 0
  $('.chat').on("click", ".my_message",function(){
    if(tmp == 0){
      tmp = 1
      id = this.id
      $("#"+id).animate({left: "100%"}, 300, function(){
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
          tmp = 0
          if(confirm("Are you sure you want to delete this message")){
            var id = $('.fa-trash').parent().attr('id')

            socket.send(JSON.stringify({"message": id, "action": "DELETE"}))
            
            $('#'+id).remove()
          }
        })
      })
    }
  }) 
  // -----------------------------------

  // ------------- Change conversation when clicking icon on the left ------------------
  $('.icon').click(function(){
    $('.chat_view').addClass('animation_hide_on_right')
    $('.input_box').addClass('animation_hide_on_right')
    $('.flip-card').hover(function(){          waiting_for_id = false
      $('.flip-card-inner').css('transform', 'none')
      $('p').css('opacity', '1')
    })
    $("#"+this.id).prependTo('.top');
    id = $(this).attr('id')
    Cookies.set('same_site', 'true');
    setTimeout(function(){
      if($('#'+id).hasClass('group_redirect')){
        window.location.href = '/group/' + id.replace('c', '').replace('g', '')
      } else {
        window.location.href = '/conversation/' + id.replace('c', '').replace('g', '')
      }
    }, 300)
  })
  // ---------------------------------------------------

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

  // ------------ Swipe right to show recent conversations on mobile ------------------
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
  // ---------------------------------------------------------------------------------------

  var elem = document.querySelector('.chat_view');
  elem.scrollTop = elem.scrollHeight;

  // -------------- Socket handling & Message receiving -------------------
  function connect() {
    socket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    socket.onmessage = function (e) {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        data = data["payload"];
        const message = JSON.parse(data['message']);
        const action = data["action"];
        const token = message.token
        if($("#"+token).length){
          $("#"+token).attr("id", message.id);
          return
        }

        switch (action) {
            case "SEND":
              if($(".chat").children().length < 3 && $('#is_group').val() != "true"){
                window.location.reload()
              }
              if($('#is_group').val() == "true"){
                $('.chat').append(
                  '<div class="message_wrapper"> \
                    <h5 class="author float-left">'+message.author+'</h5> \
                    <div class="others_message float-left message" id="'+ message.id +'">'+ message.text +'</div> \
                  </div>'
                )
              } else {
                $('.chat').append('<div class="others_message float-left message" id="'+message.id+'">'+message.text+'</div>')
                $('.chat_view').scrollTop($('.chat_view')[0].scrollHeight)
              }
              break;
            case "DELETE":
              if($('#is_group').val() == "true"){
                $('#'+message.id).parent().remove()
              } else {
                $('#'+message.id).remove()
              }
              break;
            default:
              console.log("No event")
        }
    };
  } 
  // ----------------------------------------------

  connect()
}); 

