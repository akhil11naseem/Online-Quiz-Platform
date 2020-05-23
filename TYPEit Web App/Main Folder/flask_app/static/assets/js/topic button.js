$(".topic-btn > input").click(function(){
    if($(this).prop('checked')){
        $(this).parent().removeClass("btn-outline-danger");
        $(this).parent().addClass("btn-success");
        $(this).parent().removeClass("focus");
    }
    else{
        $(this).parent().removeClass("btn-success");
        $(this).parent().addClass("btn-outline-danger");
        $(this).parent().removeClass("focus");
    }
});
