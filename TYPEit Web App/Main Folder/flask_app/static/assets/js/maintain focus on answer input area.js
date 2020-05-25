// //maintains focus on input field while user inputs answer
$('#hint-and-answer-input').on('blur', function() {
    var blurEl = $(this);
    setTimeout(function() {
        blurEl.focus()
    }, 10);
});
