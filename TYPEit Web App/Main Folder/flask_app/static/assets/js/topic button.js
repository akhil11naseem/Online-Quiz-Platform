//this controls the styles that are applied to the topic button as it is checked and unchecked
//purpose of this is to distinguish disabled and enabled buttons
$(".topic-btn > input").click(function() {
    if ($(this).prop('checked')) {
        $(this).parent().removeClass("btn-outline-danger");
        $(this).parent().addClass("btn-success");
        $(this).parent().removeClass("focus");
    } else {
        $(this).parent().removeClass("btn-success");
        $(this).parent().addClass("btn-outline-danger");
        $(this).parent().removeClass("focus");
    }
});