//initialise variables
var qnum = 0;
var points = 0;
var streak = 0;
var longestStreak = 0;
var numCorrectAnswers = 0;
var totalNumQs = 0;
//function for checking if user input matches the answer
function checkAnswer(user_answer, questions_JSON) {
    //find answer from JSON file containing questions and find total questions in set
    actual_answer = questions_JSON[qnum].Answer;
    totalNumQs = Object.keys(questions_JSON).length;
    //force lowercase and check if answer is complete
    //iterate correct answer number
    if (user_answer.toLowerCase() == actual_answer.toLowerCase()) {
        numCorrectAnswers++;
        //append to words answered list with a tick if correct

        $('#words-answered-p').text("Words answered (" + numCorrectAnswers + ")");
        $('#words-answered-col:last-child').append(
            "<p>" + questions_JSON[qnum].Answer + "  ✔<br></p>"
        );
        // streak point system awarding points the higher streak you are on

        streak++;
        points = points + streak;
        if (streak > longestStreak) longestStreak = streak;

        $("#points-h1").html(points);
        $("#streak-h1").html(streak);
        //iterate qnum and show next question
        qnum++;
        showNextQuestion(questions_JSON, totalNumQs);
    }
}
//function for the coloured line that lets players know how they are tracking with the word.
function hintLine(user_answer, questions_JSON) {
    actual_answer = (questions_JSON[qnum].Answer).toLowerCase();
    user_answer = user_answer.toLowerCase();
    hint_hr = document.getElementById('hint-hr');
    // only initialise when user inputs a value
    // if input does not start with the first letter of answer it turns red
    //if input is NOT a subset of answer, it turns red
    //else turns green
    if (user_answer.length == 0) {

        hint_hr.style.marginRight = "100%";
    } else if (actual_answer.indexOf(user_answer) != 0) {
        hint_hr.style.marginRight = "0";
        hint_hr.style.backgroundColor = "red";
    } else if (actual_answer.indexOf(user_answer) == 0) {
        scaleX = 100 - (100 * user_answer.length / actual_answer.length) + "%";
        hint_hr.style.marginRight = scaleX;
        hint_hr.style.backgroundColor = "mediumspringgreen";
    }

}
//function for loading next question into active window
function showNextQuestion(questions_JSON, totalNumQs) {
    //detecting end of line of questions
    if (qnum < totalNumQs && window.timeUP == false) {

        $('#question-text').html(questions_JSON[qnum].Question);
        $('#hint-and-answer-input').prop("value", "");
        $('#hint-and-answer-input').prop("placeholder", questions_JSON[qnum].Hint);
    } else {
        //Game over,
        //sending results to -->flask-->db,
        //then redirect to results page.
        window.timeUP = true;
        processResults();
    }
}
//function for post screen after quiz, converts points to string and converts results to 
function processResults() {
    results = [points.toString(), window.topic_name]
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=utf-8",
        url: "/update-results",
        traditional: "true",
        data: JSON.stringify({ results: results }),
        dataType: "json"
    });
    //accuracy calculator

    var accuracy = 0;
    if (totalNumQs != 0) accuracy = 100 * numCorrectAnswers / totalNumQs;
    //results2 holds values for current session converted to string for storage and manipulation

    results2 = [
        points.toString(),
        numCorrectAnswers.toString(),
        longestStreak.toString(),
        accuracy.toString(),
        document.getElementById("words-answered-row").innerHTML,
    ]
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=utf-8",
        url: "/results-page",
        traditional: "true",
        data: JSON.stringify({ results2: results2 }),
        dataType: "html",
        success: function(response) {
            document.write(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}
//skip button functionality
$("#skip-btn").click(function() {
    $('#words-answered-col:last-child').append(
        "<p>" + questions_JSON[qnum].Answer + "  ✘<br></p>"
    );
    qnum++;
    streak = 0;
    $("#streak-h1").html(streak);
    showNextQuestion(questions_JSON, Object.keys(questions_JSON).length);
});