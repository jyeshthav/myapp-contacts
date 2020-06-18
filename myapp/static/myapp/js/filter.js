function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){

    $('.modal').modal();
    $("#q").on('keyup', function() {
        const query = $(this).val();
        if (query === ''){
            location.reload();
        }
        else{
            $.ajax({
                type: 'POST',
                url: '/search_results',
                beforeSend:function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                data: {query},
                success: function(result){
                    $('#results').html(result)
                },
            });
        }
        
    });

});
