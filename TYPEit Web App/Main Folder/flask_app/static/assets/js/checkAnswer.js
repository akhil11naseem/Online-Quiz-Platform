var qnum = 0;
var points = 0;
var streak = 0;
var longestStreak = 0;
var numCorrectAnswers = 0;
var totalNumQs = 0;
function checkAnswer(user_answer, questions_JSON){

  actual_answer = questions_JSON[qnum].Answer;
  totalNumQs = Object.keys(questions_JSON).length;

  if(user_answer.toLowerCase()==actual_answer.toLowerCase()){
    numCorrectAnswers++;

    $('#words-answered-p').text("Words answered ("+ numCorrectAnswers  +")");
    $('#words-answered-col:last-child').append(
      "<p>" + questions_JSON[qnum].Answer + "  ✔<br></p>"
    );

    streak++;
    points=points+streak;
    if(streak>longestStreak) longestStreak = streak;

    $("#points-h1").html(points);
    $("#streak-h1").html(streak);

    qnum++;
    showNextQuestion(questions_JSON, totalNumQs);
  }
}

function showNextQuestion(questions_JSON, totalNumQs){

  if(qnum<totalNumQs && window.timeUP==false){

    $('#question-text').html(questions_JSON[qnum].Question);
    $('#hint-and-answer-input').prop("value", "");
    $('#hint-and-answer-input').prop("placeholder", questions_JSON[qnum].Hint);
  }
  else {
    //Game over,
    //sending results to -->flask-->db,
    //then redirect to results page.
    window.timeUP=true;
    processResults();
  }
}

function processResults(){
  results = [points.toString(), window.topic_name]
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    url: "/update-results",
    traditional: "true",
    data: JSON.stringify({results}),
    dataType: "json"
  });

  var accuracy = 0;
  if(totalNumQs!=0) accuracy = 100*numCorrectAnswers/totalNumQs;

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
    data: JSON.stringify({results2}),
    dataType: "html",
    success: function(response){
      document.write(response);
    },
    error: function(jqXHR, textStatus, errorThrown)
    {
      alert(errorThrown);
    }
  });
}

$("#skip-btn").click(function(){
  $('#words-answered-col:last-child').append(
    "<p>" + questions_JSON[qnum].Answer + "  ✘<br></p>"
  );
  qnum++;
  streak=0;
  $("#streak-h1").html(streak);
  showNextQuestion(questions_JSON, Object.keys(questions_JSON).length);
});
