function getMealRecommendations() {
    var gender = $('#gender').val();
    var age = $('#age').val();
    var weight = $('#weight').val();
    var height = $('#height').val();
    var activity = $('#activity').val();
  
    $.ajax({
      type: "POST",
      url: "/results",
      data: {gender: gender, age: age, weight: weight, height: height, activity: activity},
      success: function(response) {
        $('#response').html(response);
      }
    });
  }
  
