var names = ["Ben", "Joel", "Judy", "Anne"];
var scores = [88, 98, 77, 88];

var $ = function (id) { return document.getElementById(id); };

window.onload = function () {
	$("display_results").onclick = displayResults;
	$("display_scores").onclick = displayScores;
	$("add").onclick = addScore;
    $("name").focus();
};

function displayResults() {
    var highestScore = 0;
	var average = 0;
    for (var i = 0; i < scores.length; i++) {
        average= (average*(i)+scores[i])/(i+1);
        if (scores[i] > highestScore) {
            highestScore = scores[i];
			highestScoreName = names[i];
        }
    }
    document.getElementById("results").innerHTML = "<h2> Results </h2> Average score = " + average + "<br /> High score = " + highestScoreName + " with a score of " + highestScore;
}

function displayScores() {
    var table = document.getElementById("scores_table");
    table.innerHTML = "<h2> Scores </h2>";

	var row = table.insertRow();
	var cell1 = row.insertCell(0);
	var cell2 = row.insertCell(1);
	cell1.innerHTML = "<b> Name </b>";
	cell2.innerHTML = "<b> Score </b>";
    for (var i = 0; i < names.length; i++) {
        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = names[i];
        cell2.innerHTML = scores[i];
    }
}

function addScore() {
    var newName = $("name").value.trim();
    var newScore = parseInt($("score").value.trim());


    if (newName === "" || isNaN(newScore) || newScore < 0 || newScore > 100) {
        alert("You must enter a name and a valid score.");
        return;
    }

    names.push(newName);
    scores.push(newScore);

    $("name").value = "";
    $("score").value = "";

    $("name").focus();
}
