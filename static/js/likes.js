$('.btn-success').click(function(){
    var id = $(this).attr("data-catid");
    $.ajax(
    {
        type:"POST",
        url: "/account/like/"+id,
        data : {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        dataType : "json",
        success: function( data ){
            $('#like'+id+' span').html(data.likes)
            $('#dislike'+id+' span').html(data.dislikes)
        }
    })
});
