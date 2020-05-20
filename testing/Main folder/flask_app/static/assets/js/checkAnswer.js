var qnum = 0;
var points = 0;
var streak = 0;
var numAnswered = 0;
function checkAnswer(user_answer, questions_JSON){

  actual_answer = questions_JSON[qnum].Answer;

  if(user_answer.toLowerCase()==actual_answer.toLowerCase()){
    numAnswered++;

    $('#words-answered-p').text("Words answered ("+ numAnswered  +")");
    $('#words-answered-col:last-child').append(
      "<p>" + questions_JSON[qnum].Answer + "  ✔<br></p>"
    );

    streak++;
    points=points+streak;

    $("#points-h1").html(points);
    $("#streak-h1").html(streak);

    qnum++;
    showNextQuestion(questions_JSON);
  }
}

function showNextQuestion(questions_JSON){
  if(qnum<Object.keys(questions_JSON).length){

    $('#question-text').html(questions_JSON[qnum].Question);
    $('#hint-and-answer-input').prop("value", "");
    $('#hint-and-answer-input').prop("placeholder", questions_JSON[qnum].Hint);
  }
  else {
    results = [points.toString(), "English"]
    $.ajax({
          type: "POST",
          contentType: "application/json;charset=utf-8",
          url: "/update-results",
          traditional: "true",
          data: JSON.stringify({results}),
          dataType: "json"
          });
    window.location.replace("/results-page");
  }
}

$("#skip-btn").click(function(){
  $('#words-answered-col:last-child').append(
    "<p>" + questions_JSON[qnum].Answer + "  ✘<br></p>"
  );
  qnum++;
  streak=0;
  $("#streak-h1").html(streak);
  showNextQuestion(questions_JSON);
});
