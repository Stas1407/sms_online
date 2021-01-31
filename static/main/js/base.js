$('.search-button').click(function(){
  $(this).parent().toggleClass('open');
});

$(window).on('resize', function() {
    if($(window).width() > 1800) {
        $('#container_navbar').addClass('container-fluid');
        $('#container_navbar').removeClass('container');
    }else{
        $('#container_navbar').addClass('container');
        $('#container_navbar').removeClass('container-fluid');
    }
})

$(window).on('load', function() {
    if($(window).width() > 1800) {
        $('#container_navbar').addClass('container-fluid');
        $('#container_navbar').removeClass('container');
    }else{
        $('#container_navbar').addClass('container');
        $('#container_navbar').removeClass('container-fluid');
    }
})
