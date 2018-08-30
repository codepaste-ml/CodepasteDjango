$(function() {
    $('.to-top').hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.to-top').fadeIn();
        } else {
            $('.to-top').fadeOut();
        }
    });

    $('.to-top').on('mousedown', function(event) {
        event.preventDefault();
        $('html, body').animate({scrollTop: 0}, 800);
    });
});