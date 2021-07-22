$('.btn-secondary').click(function(){
    var id = $(this).attr("data-catid");
    $.ajax(
    {
        type:"POST",
        url: "/account/follow/"+id,
        data : {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        dataType : "json",
        success: function( data ) {
            if (data.button) {
                $('#follow span').html('Unfollow')
            }
            else {
                $('#follow span').html('Follow')
            }
        }
    })
});
