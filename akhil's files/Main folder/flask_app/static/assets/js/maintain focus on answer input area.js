$('#hint-and-answer-input').on('blur',function () { 
    var blurEl = $(this); 
    setTimeout(function() {
        blurEl.focus()
    }, 10);
});

$('#hint-and-answer-input').keyup(function() { 
    var answer = $(this).val();
    console.log('answer = ' + answer);
    $(this).val(answer);
    $(this).attr("value", answer);
});
