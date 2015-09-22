function get_diff(){
    var start = parseInt($('#quantity').text());
    $.ajax({
        url: "/requests/",
        type: 'post',
        data: {"start_request": start},
        success: function(diff){
            $('title').text(diff);
        }
    })
}

$(document).ready(function(){

    setInterval('get_diff()',1000);

});

